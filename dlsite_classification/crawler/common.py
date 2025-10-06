import asyncio
import logging
from collections.abc import Iterable
from typing import Any

import aiohttp
from bs4 import BeautifulSoup

from dlsite_classification.common.net import HEADERS
from dlsite_classification.spkg.logs import Green


class CommonCrawler:
    @classmethod
    async def get_image(
        cls, session: aiohttp.ClientSession, url: str
    ) -> dict[str, Any]:
        async with session.get(url) as response:
            Green(logging.info, f"Get image name {response.url.raw_name}")
            img = await response.content.read()
            return {"data": img, "url": url, "name": response.url.raw_name}

    @classmethod
    async def get_images(cls, urls: Iterable[str]) -> tuple[dict[str, Any], ...]:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            results = await asyncio.gather(
                *[cls.get_image(session, url) for url in urls]
            )
            return tuple(results)

    @classmethod
    async def get_request(
        cls, url: str, is_json: bool = False
    ) -> tuple[str, BeautifulSoup] | dict[str, Any]:
        """Return tuple html and bs4."""

        async with (
            aiohttp.ClientSession(headers=HEADERS) as session,
            session.get(url) as response,
        ):
            if response.status == 200:
                if is_json:
                    return await response.json()
                html = await response.text()
                bs4 = BeautifulSoup(html, "lxml")
            else:
                raise ValueError(f"{url} Request Fail!!")
        return html, bs4
