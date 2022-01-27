import signal
import asyncio
import logging


class SAsync:

    def __init__(self, main_run=None, loop=None):
        if loop is None:
            try:
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop
        # -----------------------
        if self.add_signal():
            return None
        # -----------------------
        self.main_run = main_run

    def stop_loop_on_completion(self, f):
        self.loop.stop()

    def register_run(self, run_func):
        self.main_run = run_func

    def run(self, *args, **kwargs) -> None:

        async def runner():
            await self.main_run(*args, **kwargs)

        if self.main_run is None:
            raise ValueError("NotRunningFunction")

        future = asyncio.ensure_future(runner(), loop=self.loop)
        future.add_done_callback(self.stop_loop_on_completion)

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            logging.info('Received signal to terminate bot and event loop.')
        finally:
            future.remove_done_callback(
                self.stop_loop_on_completion
            )
            logging.info('Cleaning up tasks.')
            self._clean_up()

    def _clean_up(self) -> None:
        pending = [
            task
            for task
            in asyncio.all_tasks(loop=self.loop)
            if not task.done()
        ]

        if not pending:
            return

        logging.info(f'Cleaning up after {len(pending)} tasks.')
        for task in pending:
            task.cancel()

        self.loop.run_until_complete(
            asyncio.gather(
                *pending,
                return_exceptions=True
            )
        )

        logging.info('All tasks finished cancelling.')

        self.loop.run_until_complete(
            self.loop.shutdown_asyncgens()
        )
        self.loop.run_until_complete(
            self.loop.shutdown_default_executor()
        )
        self.loop.close()

    def add_signal(self) -> bool:
        try:
            self.loop.add_signal_handler(
                signal.SIGINT,
                lambda: self.loop.stop()
            )
            self.loop.add_signal_handler(
                signal.SIGTERM,
                lambda: self.loop.stop()
            )
            return True
        except NotImplementedError:
            return False
