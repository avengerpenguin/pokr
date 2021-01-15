import os
from datetime import datetime

import cachetools

from . import Metric

CACHE = cachetools.TTLCache(maxsize=256, ttl=900)


@cachetools.cached(CACHE)
def _get_items_projects():
    from todoist.api import TodoistAPI

    api = TodoistAPI(os.getenv("TODOIST_TOKEN"))
    api.sync()
    return list(api.state["items"]), list(api.state["projects"])


def items(project_name=None, priority=None, checked=0, title=None):
    def due(date_obj):
        if not date_obj:
            return True
        today = datetime.today()
        due_date = datetime.strptime(date_obj["date"], "%Y-%m-%d")
        return today > due_date

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
                    if not priority
                    or i["priority"] == priority
                    and (not title or i["content"] == title)
                    and (checked or due(i["due"]))
                    and i["checked"] == checked
                )
            )

    return Metric(f)
