import asyncio
import os
from typing import Any, Callable, Coroutine, Dict, List

from invoke import Collection, Task, task
from quart import Quart, render_template

__all__ = ["app", "invoke", "metrics"]


async def task_tuple(name: str, coro: Callable[[], Coroutine]):
    return name, await coro()


def app(
    name: str,
    metric_functions: Dict[str, Dict[str, Callable[[], Coroutine]]],
) -> Quart:
    template_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "templates"
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


def add_task(collection: Collection, t: Task, **project_args) -> None:
    @task(
        name=t.name,
        optional=t.optional,
    )
    def wrapped_task(c, **task_args):
        return t(c, **project_args, **task_args)

    wrapped_task.__doc__ = t.__doc__
    collection.add_task(wrapped_task, name=t.__name__)


def invoke() -> Collection:
    from . import tasks as t

    collection = Collection("tasks")
    add_task(collection, t.livereload)
    return collection
