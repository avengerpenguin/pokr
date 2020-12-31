# import asyncio
# import os
# from collections import namedtuple
# import aiohttp
# import aiohttp_jinja2
# import functools
# import jinja2
# from accept_types import get_best_match
# from aiohttp import web
# from aiohttp_jinja2_haggle import negotiate
#
#
#
#
# @negotiate('scorecard.html')
# async def index(request):
#     kpi_tasks = [
#         security(),
#         reach(),
#         product(),
#     ]
#
#     kpis = sum(await asyncio.gather(*kpi_tasks), [])
#
#     return {'kpis': kpis}
#
#
# def application(loop=None):
#     app = web.Application(loop=loop)
#     aiohttp_jinja2.setup(
#         app,
#         loader=jinja2.FileSystemLoader(os.path.join(
#             os.path.abspath(os.path.dirname(__file__)),
#             'templates')))
#
#     app.router.add_get('/', index)
#
#     return app
import asyncio
import os
from collections import defaultdict

from invoke import task, Collection
from quart import Quart, render_template

from . import metrics

__all__ = ["app", "invoke", "metrics"]


def app(name, metrics=None):
    template_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'templates')
    quart_app = Quart(name, template_folder=template_dir)
    quart_app.config.from_mapping(debug=True)

    @quart_app.route("/")
    async def index():
        scorecard = {}

        for heading, kpis in metrics.items():
            scorecard[heading] = []

            async def f(name, gen):
                if asyncio.iscoroutinefunction(gen):
                    return name, await gen()
                else:
                    return name, gen()

            tasks = []
            for kpi, gen in kpis.items():
                tasks.append(asyncio.create_task(f(kpi, gen)))

            for coro in asyncio.as_completed(tasks):
                name, metric = await coro

                scorecard[heading].append(dict(name=name, **metric))

        return await render_template("scorecard.html", scorecard=scorecard)

    return quart_app


def add_task(TASKS, t, **project_args):
    @task(
        name=t.name, optional=t.optional,
    )
    def wrapped_task(c, **task_args):
        return t(c, **project_args, **task_args)

    wrapped_task.__doc__ = t.__doc__
    TASKS.add_task(wrapped_task, name=t.__name__)


def invoke():
    from . import tasks as t
    TASKS = Collection("tasks")
    add_task(TASKS, t.livereload)
    return TASKS
