from aiofile import AIOFile, Writer


async def save_data(name: str, data):
    async with AIOFile(name, 'wb', encoding='utf-8') as afp:
        writer = Writer(afp)
        await writer(data)


async def raed_data(name: str) -> str:
    async with AIOFile(name, 'r', encoding='utf-8') as afp:
        return str(await afp.read())
