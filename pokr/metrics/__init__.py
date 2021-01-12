import asyncio
import os
from collections import defaultdict
from datetime import datetime, timedelta, date, tzinfo
from typing import Callable, Union, Text, Dict, Tuple, Awaitable

import aiohttp
import pytz
import requests
from bs4 import BeautifulSoup
from github import Github
import cachetools
import math
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


CACHE = cachetools.TTLCache(maxsize=256, ttl=900)


class Metric(object):
    def __init__(self, v: Callable[[], Awaitable[Union[int, float]]]):
        self.v = v

    def __call__(self) -> Awaitable[Union[int, float]]:
        return self.v()

    def __ge__(self, thresholds: Tuple[Union[int, float], Union[int, float]]) -> Callable[[], Awaitable[Dict]]:
        amber, green = thresholds

        async def f() -> Dict:
            if asyncio.iscoroutinefunction(self.v):
                v = await self.v()
            else:
                v = self.v()

            if v >= green:
                status = 'green'
            elif v >= amber:
                status = 'amber'
            else:
                status = 'red'

            return {
                'status': status,
                'value': v,
                'green': green,
                'amber': amber,
            }

        return f

    def __le__(self, thresholds: Tuple[Union[int, float], Union[int, float]]) -> Callable[[], Awaitable[Dict]]:
        green, amber = thresholds

        async def f() -> Dict:
            if asyncio.iscoroutinefunction(self.v):
                v = await self.v()
            else:
                v = self.v()

            if v <= green:
                status = 'green'
            elif v <= amber:
                status = 'amber'
            else:
                status = 'red'

            return {
                'status': status,
                'value': v,
                'green': green,
                'amber': amber,
            }

        return f


async def _fetch(session: aiohttp.ClientSession, url: Text) -> Text:
    async with session.get(url) as response:
        return await response.text()


def fetch(url: Text, parser: Callable) -> Metric:
    async def f():
        async with aiohttp.ClientSession() as session:
            text = await _fetch(session, url)
            soup = BeautifulSoup(text, 'html.parser')
            return parser(soup)

    return Metric(f)


def goodreads(user: Text):
    url = f"https://www.goodreads.com/review/list/{user}?shelf=read"
    return fetch(
        url,
        lambda soup: int(
            soup.select("#header > h1 > span > span")[0].string.rstrip(')').lstrip('(')
        )
    )


def notes(repo_name):
    github = Github(os.getenv('GITHUB_TOKEN'))
    repo = github.get_repo(repo_name)

    async def f():
        contents = repo.get_contents("")

        word_count = 0

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.name.endswith(".md"):
                word_count += len(file_content.decoded_content.decode('utf8').replace('#', '').lstrip().split(' '))

        return word_count

    return Metric(f)


def libraries(user_id):
    url = f'https://libraries.io/api/github/{user_id}/projects?api_key={os.getenv("LIBRARIES_API_KEY")}'

    async def f():
        last_release = pytz.utc.localize(datetime.now()) - timedelta(days=10000)

        r = requests.get(url)
        r.raise_for_status()
        projects = r.json()

        for project in projects:
            published = datetime.strptime(project['latest_release_published_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
            last_release = max(last_release, published)

        return (pytz.utc.localize(datetime.now()) - last_release).days

    return Metric(f)


def sourcerank(user_id):
    url = f'https://libraries.io/api/github/{user_id}/projects?api_key={os.getenv("LIBRARIES_API_KEY")}'

    async def f():
        last_release = pytz.utc.localize(datetime.now()) - timedelta(days=10000)

        r = requests.get(url)
        r.raise_for_status()
        projects = r.json()

        for project in projects:
            published = datetime.strptime(project['latest_release_published_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
            last_release = max(last_release, published)

        ranks = [project['rank'] for project in projects]
        return round(sum(ranks) / len(ranks), 2)

    return Metric(f)


def notmuch():
    from sh import notmuch

    async def f():
        return int(notmuch(['count', 'tag:inbox']).strip())

    return Metric(f)


def sheet_value(sheet_id, range):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-sheets.pickle'):
        with open('token-sheets.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token-sheets.pickle', 'wb') as token:
            pickle.dump(creds, token)

    async def f():
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
        values = result.get('values', [])
        return float(values[0][0].replace('£', ''))

    return Metric(f)


def sheet_tracker(sheet_id, habit="Exercise"):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-sheets.pickle'):
        with open('token-sheets.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token-sheets.pickle', 'wb') as token:
            pickle.dump(creds, token)

    @cachetools.cached(CACHE)
    def sheet_data():
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range='A1:AH110').execute()
        values = result.get('values', [])
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

                if habit_status == 'TRUE':
                    habit_counts[habit_name] += 1

        return habit_counts[habit]

    return Metric(f)


def baseline(metric, base):
    async def f():
        n = await metric()
        return n - base

    return Metric(f)


def scaled(thresholds, start, deadline):
    now = date.today()
    elapsed = (now - start) / (deadline - start)
    t1, t2 = thresholds
    return math.floor(t1 * elapsed), math.ceil(t2 * elapsed)
