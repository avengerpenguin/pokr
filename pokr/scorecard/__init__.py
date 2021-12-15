import asyncio
import os
from typing import Any, Callable, Coroutine, Dict, List

from doctrine import add_task
from invoke import Collection
from quart import Quart, render_template

__all__ = ["app", "invoke"]


async def task_tuple(name: str, coro: Callable[[], Coroutine]):
    return name, await coro()


def app(
    name: str,
    metric_functions: Dict[str, Dict[str, Callable[[], Coroutine]]],
) -> Quart:
    template_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "scorecard/templates"
    )
    quart_app = Quart(name, template_folder=template_dir)
    quart_app.config.from_mapping(debug=True)

    @quart_app.route("/")
    async def index() -> str:
        scorecard: Dict[str, List[Any]] = {}

        kpis: Dict[str, Callable[[], Coroutine]]
        for heading, kpis in metric_functions.items():
            scorecard[heading] = []

            tasks = []
            for kpi, gen in kpis.items():
                tasks.append(asyncio.create_task(task_tuple(kpi, gen)))

            for coro in asyncio.as_completed(tasks):
                metric_name, metric = await coro

                scorecard[heading].append(dict(name=metric_name, **metric))

        return await render_template("scorecard.html", scorecard=scorecard)

    return quart_app


def invoke() -> Collection:
    from . import tasks as t

    collection = Collection("tasks")
    add_task(collection, t.livereload)
    return collection
