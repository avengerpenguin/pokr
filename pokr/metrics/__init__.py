import math
import os
import os.path
import pickle
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Awaitable, Callable, Dict, Tuple, Union

import aiohttp
import cachetools
import pytz
import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
from github import Github
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CACHE: TTLCache = cachetools.TTLCache(maxsize=256, ttl=900)


def scale_colour(base: str, target: str, proportion: float):
    return "".join(
        "%0.2X"
        % int(
            (
                proportion
                * (int(target[i : i + 2], 16) - int(base[i : i + 2], 16))
            )
            + int(base[i : i + 2], 16)
        )
        for i in (0, 2, 4)
    )


class Metric:
    def __init__(
        self, metric_function: Callable[[], Awaitable[Union[int, float]]]
    ):
        self.metric_function = metric_function

    def __call__(self) -> Awaitable[Union[int, float]]:
        return self.metric_function()

    def __ge__(
        self, thresholds: Tuple[Union[int, float], Union[int, float]]
    ) -> Callable[[], Awaitable[Dict]]:
        amber, green = thresholds

        async def f() -> Dict:
            v = await self()

            mid = (amber + green) / 2

            if v >= green:
                status = "green"
                colour = "2ECC40"
                hue = 120
            elif v >= amber:
                status = "amber"
                hue = int(120 * ((v - amber) / (green - amber)))
                if v >= mid:
                    colour = scale_colour(
                        "FF4136", "2ECC40", (v - mid) / (green - mid)
                    )
                else:
                    colour = scale_colour(
                        "FF4136", "FFBF00", (v - amber) / (mid - amber)
                    )
            else:
                status = "red"
                colour = "FF4136"
                hue = 0
            return {
                "status": status,
                "value": v,
                "green": green,
                "amber": amber,
                "colour": colour,
                "hue": hue,
            }

        return f

    def __le__(
        self, thresholds: Tuple[Union[int, float], Union[int, float]]
    ) -> Callable[[], Awaitable[Dict]]:
        green, amber = thresholds

        async def f() -> Dict:
            v = await self()

            if v <= green:
                status = "green"
                hue = 120
            elif v <= amber:
                status = "amber"
                hue = int(120 * ((amber - v) / (amber - green)))
            else:
                status = "red"
                hue = 0

            return {
                "status": status,
                "value": v,
                "green": green,
                "amber": amber,
                "hue": hue,
            }

        return f

    def __add__(self, other):
        async def f():
            v1 = await self()
            v2 = await other()
            return v1 + v2

        return Metric(f)


async def _fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


def fetch(url: str, parser: Callable) -> Metric:
    async def f():
        async with aiohttp.ClientSession() as session:
            text = await _fetch(session, url)
            soup = BeautifulSoup(text, "html.parser")
            return parser(soup)

    return Metric(f)


def goodreads(user: str):
    url = f"https://www.goodreads.com/review/list/{user}?shelf=read"
    return fetch(
        url,
        lambda soup: int(
            soup.select("#header > h1 > span > span")[0]
            .string.rstrip(")")
            .lstrip("(")
        ),
    )


def notes(repo_name, extension=".md"):
    github = Github(os.getenv("GITHUB_TOKEN"))
    repo = github.get_repo(repo_name)

    async def f():
        contents = repo.get_contents("")

        word_count = 0

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.name.endswith(extension):
                word_count += len(
                    file_content.decoded_content.decode("utf8")
                    .replace("#", "")
                    .lstrip()
                    .split(" ")
                )

        return word_count

    return Metric(f)


def libraries(user_id):
    url = f'https://libraries.io/api/github/{user_id}/projects?api_key={os.getenv("LIBRARIES_API_KEY")}'

    async def f():
        last_release = pytz.utc.localize(datetime.now()) - timedelta(
            days=10000
        )

        r = requests.get(url)
        r.raise_for_status()
        projects = r.json()

        for project in projects:
            published = datetime.strptime(
                project["latest_release_published_at"],
                "%Y-%m-%dT%H:%M:%S.%f%z",
            )
            last_release = max(last_release, published)

        return (pytz.utc.localize(datetime.now()) - last_release).days

    return Metric(f)


def sourcerank(user_id):
    url = f'https://libraries.io/api/github/{user_id}/projects?api_key={os.getenv("LIBRARIES_API_KEY")}'

    async def f():
        last_release = pytz.utc.localize(datetime.now()) - timedelta(
            days=10000
        )

        r = requests.get(url)
        r.raise_for_status()
        projects = r.json()

        for project in projects:
            published = datetime.strptime(
                project["latest_release_published_at"],
                "%Y-%m-%dT%H:%M:%S.%f%z",
            )
            last_release = max(last_release, published)

        ranks = [project["rank"] for project in projects]
        return round(sum(ranks) / len(ranks), 2)

    return Metric(f)


def notmuch():
    from sh import notmuch

    async def f():
        return int(notmuch(["count", "tag:inbox"]).strip())

    return Metric(f)


def git_summary():
    from sh import git_summary

    async def f():
        return len(git_summary(["-q", "-n"]))

    return Metric(f)


def sheet_value(sheet_id, range):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token-sheets.pickle"):
        with open("token-sheets.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token-sheets.pickle", "wb") as token:
            pickle.dump(creds, token)

    async def f():
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
        )
        values = result.get("values", [])
        return float(values[0][0].replace("£", ""))

    return Metric(f)


def sheet_tracker(sheet_id, habit="Exercise"):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token-sheets.pickle"):
        with open("token-sheets.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token-sheets.pickle", "wb") as token:
            pickle.dump(creds, token)

    @cachetools.cached(CACHE)
    def sheet_data():
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=sheet_id, range="A1:AH110")
            .execute()
        )
        values = result.get("values", [])
        return values

    async def f():
        values = sheet_data()
        habit_counts = defaultdict(int)

        for thedate in (date.today() - timedelta(n) for n in range(7)):
            month_row = thedate.month * 9 - 9
            day_col = thedate.day

            for habit_index in range(2, 8):
                habit_name = values[month_row + habit_index][0]
                habit_status = values[month_row + habit_index][day_col]

                if habit_status == "TRUE":
                    habit_counts[habit_name] += 1

        return habit_counts[habit]

    return Metric(f)


def baseline(metric, base):
    async def f():
        n = await metric()
        return n - base

    return Metric(f)


def scaled(thresholds, start, deadline):
    end_of_day = date.today() + timedelta(days=1)
    elapsed = (end_of_day - start) / (deadline - start)
    t1, t2 = thresholds
    return math.floor(t1 * elapsed), math.ceil(t2 * elapsed)
