import os
from datetime import timedelta, datetime

import cachetools
from github import Github

from . import Metric

github = Github(os.getenv('GITHUB_TOKEN'))
CACHE = cachetools.TTLCache(maxsize=256, ttl=900)


@cachetools.cached(CACHE)
def get_user_login():
    return github.get_user().login


@cachetools.cached(CACHE)
def get_events(cutoff):
    named_user = github.get_user(get_user_login())
    since = datetime.now() - cutoff
    feed = named_user.get_events()
    return list(
        e for e in feed
        if e.created_at > since
    )


def activity(org=None, owner=None, cutoff=timedelta(days=7)):

    async def f():
        events = get_events(cutoff)
        filtered = [
            e for e in events
            # Owner of repo much match iff owner arg specified
            if (not owner or e.repo.owner.login == owner)
            # Org of repo must match iff org arg specified
            and (not org or (e.repo.organization and e.repo.organization.login == org))
        ]

        return len(filtered)

    return Metric(f)
