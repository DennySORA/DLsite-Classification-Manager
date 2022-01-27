import asyncio
import logging
from async_timeout import timeout


class SAsyncRunner:

    def __init__(self, loop=None):
        if loop is None:
            self.loop = asyncio.get_event_loop()

        self.read = asyncio.Queue()
        self.finish = asyncio.Queue()

    def get_read_queue(self):
        return self.read

    def get_finish_queue(self):
        return self.finish

    async def run(self, count: int):
        task = [
            self.loop.create_task(
                self.run_pool(i)
            )
            for i in range(count)
        ]
        await asyncio.wait(task)

    async def run_pool(self, number: int):
        logging.info(f"{number} Pool Running.")
        while True:
            try:
                try:
                    async with timeout(3):
                        component = await self.read.get()
                except asyncio.TimeoutError:
                    logging.info(f"{number} Pool Close.")
                    return None
                await component()
                await self.finish.put(component)
                logging.info(f"{number} Pool Finish.")
            except asyncio.CancelledError:
                return None
            except BaseException as e:
                logging.error(e, exc_info=True)
