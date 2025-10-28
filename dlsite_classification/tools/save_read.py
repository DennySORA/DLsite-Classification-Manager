from aiofile import AIOFile, Writer


WritableData = str | bytes


async def save_data(name: str, data: WritableData) -> None:
    async with AIOFile(name, "wb", encoding="utf-8") as afp:
        writer = Writer(afp)
        await writer(data)


async def raed_data(name: str) -> str:
    async with AIOFile(name, "r", encoding="utf-8") as afp:
        result = await afp.read()
        return str(result)
