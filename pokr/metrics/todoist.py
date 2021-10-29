import os
from datetime import date, datetime

import cachetools

from . import Metric

CACHE = cachetools.TTLCache(maxsize=1024, ttl=900)


@cachetools.cached(CACHE)
def _get_items_projects():
    from todoist.api import TodoistAPI

    api = TodoistAPI(os.getenv("TODOIST_TOKEN"))
    api.sync()
    return list(api.state["items"]), list(api.state["projects"])


def items(
    project_name=None, priority=None, checked=0, title=None, done_since=None
):
    def due(date_obj):
        if not date_obj:
            return True
        today = date.today()
        date_string = date_obj["date"]
        if "T" in date_string:
            due_date = datetime.strptime(
                date_obj["date"], "%Y-%m-%dT%H:%M:%S"
            ).date()
        else:
            due_date = datetime.strptime(date_obj["date"], "%Y-%m-%d").date()
        return today >= due_date

    def completed_after(item, cutoff):
        date_string = item["date_completed"]
        if not date_string:
            return False
        completed_date = datetime.strptime(
            date_string, "%Y-%m-%dT%H:%M:%SZ"
        ).date()
        return completed_date >= cutoff

    async def f():
        items, projects = _get_items_projects()
        project = None
        if project_name:
            for project in projects:
                if project["name"] == project_name:
                    break

        if project_name and project:
            return len(
                list(
                    i
                    for i in items
                    if i["project_id"] == project["id"]
                    and (not priority or i["priority"] == priority)
                    and (not title or i["content"] == title)
                    and (not done_since or completed_after(i, done_since))
                    and (checked or due(i["due"]))
                    and i["checked"] == checked
                )
            )
        elif project_name:
            return 0
        else:
            return len(
                list(
                    i
                    for i in items
                    if (not priority or i["priority"] == priority)
                    and (not title or i["content"] == title)
                    and (checked or due(i["due"]))
                    and i["checked"] == checked
                )
            )

    return Metric(f)
