import os
from aiofile import async_open


async def copy_data(origin_path: str, new_path: str):
    if not os.path.isfile(origin_path):
        raise FileNotFoundError(f"{origin_path} not found")
    async with async_open(origin_path, "rb") as src:
        async with async_open(new_path, "wb") as dest:
                await dest.write(await src.read())
