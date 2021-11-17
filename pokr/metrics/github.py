import os
from datetime import datetime, timedelta

import cachetools
from cachetools import TTLCache
from github import Github

from . import Metric

github = Github(os.getenv("GITHUB_TOKEN"))
CACHE: TTLCache = cachetools.TTLCache(maxsize=256, ttl=900)


@cachetools.cached(CACHE)
def get_user_login():
    return github.get_user().login


@cachetools.cached(CACHE)
def get_events(cutoff):
    named_user = github.get_user(get_user_login())
    since = datetime.now() - cutoff
    feed = named_user.get_events()
    return list(e for e in feed if e.created_at > since)


def activity(org=None, owner=None, cutoff=timedelta(days=7)):
    async def f():
        events = get_events(cutoff)
        filtered = [
            e
            for e in events
            # Owner of repo much match iff owner arg specified
            if (not owner or e.repo.owner.login == owner)
            # Org of repo must match iff org arg specified
            and (
                not org
                or (e.repo.organization and e.repo.organization.login == org)
            )
        ]

        return len(filtered)

    return Metric(f)


def failures():
    async def f():
        named_user = github.get_user(get_user_login())

        failures = 0

        for repo in named_user.get_repos():
            trunk = repo.get_branch(repo.default_branch)
            for run in trunk.commit.get_check_runs():
                if run.conclusion != "success":
                    print(repo.name, run.name, run.conclusion)
                    failures += 1
                    break

        return failures

    return Metric(f)


def pulls():
    async def f():
        github.get_user(get_user_login())

    return Metric(f)
