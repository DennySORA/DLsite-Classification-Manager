import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from async_timeout import timeout


AsyncFunction = Callable[[], Awaitable[Any]]


class SAsyncRunner:
    def __init__(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self.read: asyncio.Queue[AsyncFunction] = asyncio.Queue()
        self.finish: asyncio.Queue[AsyncFunction] = asyncio.Queue()

    def get_read_queue(self) -> asyncio.Queue[AsyncFunction]:
        return self.read

    def get_finish_queue(self) -> asyncio.Queue[AsyncFunction]:
        return self.finish

    async def run(self, count: int) -> None:
        tasks = [self.loop.create_task(self.run_pool(i)) for i in range(count)]
        await asyncio.wait(tasks)

    async def run_pool(self, number: int) -> None:
        logging.info(f"{number} Pool Running.")
        while True:
            try:
                try:
                    async with timeout(3):
                        component = await self.read.get()
                except asyncio.TimeoutError:
                    logging.info(f"{number} Pool Close.")
                    return
                await component()
                await self.finish.put(component)
                logging.info(f"{number} Pool Finish.")
            except asyncio.CancelledError:
                return
            except BaseException as exc:
                logging.error(exc, exc_info=True)
