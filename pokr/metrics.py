import asyncio

import aiohttp
from bs4 import BeautifulSoup


class Metric(object):
    def __init__(self, v):
        self.v = v

    def __ge__(self, thresholds):
        amber, green = thresholds

        async def f():
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
            }

        return f


async def _fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def fetch(url):
    async def f():
        async with aiohttp.ClientSession() as session:
            text = await _fetch(session, url)
            soup = BeautifulSoup(text, 'html.parser')
            return int(soup.select("#header > h1 > span > span")[0].string.rstrip(')').lstrip('('))

    return Metric(f)


def fetch2():
    return Metric(lambda: 8)
