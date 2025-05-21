import uvicorn

from fastapi import FastAPI
from fastapi.responses import FileResponse

from dlsite_classification.extract.extract import ExtractFolder

app = FastAPI()
extract_data = ExtractFolder()


@app.get("/")
async def all_data(limit: int = 10, offset: int = 0):
    if limit == -1:
        return extract_data.get_all_table()
    return extract_data.get_table(limit, offset)


@app.get("/image")
async def get_image(path: str):
    return FileResponse(path)


@app.get("/scan")
async def scan():
    use_time = await extract_data.scan_file()
    return {"status": "ok", "scan_time": use_time}

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=80,
        log_level="info"
    )
