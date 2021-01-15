from typing import Awaitable, Callable, Union

import pytest

from pokr.metrics import Metric


@pytest.fixture
def gen() -> Callable[[], Awaitable[Union[int, float]]]:
    async def f():
        return 123

    return f


@pytest.mark.asyncio
async def test_metric_call(gen):
    m = Metric(gen)
    assert 123 == await m()


@pytest.mark.asyncio
async def test_gte_metric_green(gen):
    m = Metric(gen)
    kpi_function = m >= (50, 100)
    kpi = await kpi_function()

    assert kpi["status"] == "green"


@pytest.mark.asyncio
async def test_lte_metric_green(gen):
    m = Metric(gen)
    kpi_function = m <= (200, 250)
    kpi = await kpi_function()

    assert kpi["status"] == "green"
