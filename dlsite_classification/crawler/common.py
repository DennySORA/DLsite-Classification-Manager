import logging
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from typing import Union

from dlsite_classification.spkg.logs import Green
from dlsite_classification.common.net import HEADERS


class CommonCrawler:

    @classmethod
    async def get_image(cls, session, url: str) -> dict:
        async with session.get(url) as response:
            Green(
                logging.info,
                f"Get image name {response.url.raw_name}"
            )
            img = await response.content.read()
            return {
                'data': img,
                'url': url,
                'name': response.url.raw_name
            }

    @classmethod
    async def get_images(cls, urls) -> tuple[dict]:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            return await asyncio.gather(
                *[
                    cls.get_image(session, url) for url in urls
                ]
            )

    @classmethod
    async def get_request(cls, url: str,is_json=False) -> Union[tuple[str, BeautifulSoup],dict]:
        """Return tuple html and bs4."""

        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    if is_json:
                        return await response.json()
                    html = await response.text()
                    bs4 = BeautifulSoup(html, 'lxml')
                else:
                    raise ValueError(f"{url} Request Fail!!")
        return html, bs4
