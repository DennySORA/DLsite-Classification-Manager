"""Integration tests hitting DLsite with real requests."""
import asyncio
import re

import aiohttp
import pytest
import pytest_asyncio

from dlsite_classification.common.dlsite import BJ_WEBPATH, RJ_WEBPATH, VJ_WEBPATH
from dlsite_classification.common.net import HEADERS
from dlsite_classification.crawler.work import DLsiteWorkCrawler


NEW_RELEASE_PAGES: dict[str, str] = {
    "rj": "maniax",
    "bj": "books",
    "vj": "pro",
}
CODE_PATTERNS: dict[str, re.Pattern[str]] = {
    "rj": re.compile(r"RJ\d{6,8}"),
    "bj": re.compile(r"BJ\d{6,8}"),
    "vj": re.compile(r"VJ\d{6,8}"),
}

_CODE_CACHE: dict[str, str] = {}
_CRAWLER_CACHE: dict[str, DLsiteWorkCrawler] = {}


@pytest.fixture(autouse=True)
def _suppress_logging(disable_logging):
    yield


async def _fetch_latest_code(kind: str) -> str:
    page = NEW_RELEASE_PAGES[kind]
    url = f"https://www.dlsite.com/{page}/new"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError(f"{url} responded with {response.status}")
            text = await response.text()
    matches = CODE_PATTERNS[kind].findall(text)
    if not matches:
        raise RuntimeError(f"Could not find {kind.upper()} code on {url}")
    return matches[0]


@pytest_asyncio.fixture
async def latest_dlsite_codes() -> dict[str, str]:
    if not _CODE_CACHE:
        tasks = {kind: asyncio.create_task(_fetch_latest_code(kind)) for kind in NEW_RELEASE_PAGES}
        for kind, task in tasks.items():
            _CODE_CACHE[kind] = await task
    return dict(_CODE_CACHE)


@pytest_asyncio.fixture
async def rj_crawler(latest_dlsite_codes):
    code = latest_dlsite_codes["rj"]
    cached = _CRAWLER_CACHE.get(code)
    if cached is None:
        crawler = DLsiteWorkCrawler(code=code)
        await crawler.get_use_code()
        _CRAWLER_CACHE[code] = crawler
        return crawler
    return cached


@pytest_asyncio.fixture
async def bj_crawler(latest_dlsite_codes):
    code = latest_dlsite_codes["bj"]
    cached = _CRAWLER_CACHE.get(code)
    if cached is None:
        crawler = DLsiteWorkCrawler(code=code)
        await crawler.get_use_code()
        _CRAWLER_CACHE[code] = crawler
        return crawler
    return cached


@pytest_asyncio.fixture
async def vj_crawler(latest_dlsite_codes):
    code = latest_dlsite_codes["vj"]
    cached = _CRAWLER_CACHE.get(code)
    if cached is None:
        crawler = DLsiteWorkCrawler(code=code)
        await crawler.get_use_code()
        _CRAWLER_CACHE[code] = crawler
        return crawler
    return cached


@pytest.fixture
def rj_info(rj_crawler):
    return rj_crawler.get_info()


@pytest.fixture
def bj_info(bj_crawler):
    return bj_crawler.get_info()


@pytest.fixture
def vj_info(vj_crawler):
    return vj_crawler.get_info()


@pytest.mark.integration
@pytest.mark.slow
class TestRealDLsiteCrawler:
    async def test_crawl_real_rj_code(self, latest_dlsite_codes, rj_info):
        assert rj_info is not None
        assert rj_info.get("code") == latest_dlsite_codes["rj"]
        assert isinstance(rj_info.get("title"), list)
        assert rj_info["title"][0]
        assert rj_info["title"][1] == f"{RJ_WEBPATH}{latest_dlsite_codes['rj']}"
        assert isinstance(rj_info.get("company"), list)
        assert rj_info["company"][0]
        assert isinstance(rj_info.get("introduction"), str)
        assert isinstance(rj_info.get("images"), tuple)
        assert len(rj_info["images"]) >= 1

    async def test_crawl_real_bj_code(self, latest_dlsite_codes, bj_info):
        assert bj_info is not None
        assert bj_info.get("code") == latest_dlsite_codes["bj"]
        assert bj_info["title"][1] == f"{BJ_WEBPATH}{latest_dlsite_codes['bj']}"
        assert isinstance(bj_info.get("images"), tuple)
        assert len(bj_info["images"]) >= 1

    async def test_crawl_real_vj_code(self, latest_dlsite_codes, vj_info):
        assert vj_info is not None
        assert vj_info.get("code") == latest_dlsite_codes["vj"]
        assert vj_info["title"][1] == f"{VJ_WEBPATH}{latest_dlsite_codes['vj']}"
        assert isinstance(vj_info.get("images"), tuple)
        assert len(vj_info["images"]) >= 1


@pytest.mark.integration
@pytest.mark.slow
class TestHTMLStructureValidation:
    async def test_bs4_is_populated(self, rj_crawler):
        assert rj_crawler.bs4 is not None

    async def test_title_selector_valid(self, rj_crawler):
        title_tag = rj_crawler.bs4.find("h1")
        assert title_tag is not None
        text = title_tag.text.replace("\n", "")
        assert text

    async def test_metadata_container_present(self, rj_crawler):
        metadata_div = rj_crawler.bs4.find(id="work_right_inner")
        assert metadata_div is not None
        outline_table = metadata_div.find("table", id="work_outline")
        assert outline_table is not None
        assert outline_table.find_all("tr")

    async def test_images_container_present(self, rj_crawler):
        slider = rj_crawler.bs4.find("div", "product-slider-data")
        assert slider is not None
        assert any(div.get("data-src") for div in slider.find_all("div"))


@pytest.mark.integration
@pytest.mark.slow
class TestDataFormatValidation:
    async def test_info_structure(self, rj_info):
        non_list_fields = {"title", "code", "company", "introduction", "images"}
        for key, value in rj_info.items():
            if key in {"title", "company"}:
                assert isinstance(value, list)
                assert all(isinstance(item, str) for item in value)
            elif key == "images":
                assert isinstance(value, tuple)
            elif key not in non_list_fields:
                assert isinstance(value, list)
                assert all(isinstance(item, str) for item in value)

    async def test_image_payload(self, rj_info):
        for image in rj_info["images"]:
            assert isinstance(image, dict)
            assert isinstance(image.get("data"), bytes)
            assert image.get("data")
            url = image.get("url")
            assert isinstance(url, str)
            assert url.startswith("https:")
            assert image.get("name")


@pytest.mark.unit
class TestCrawlerErrorDetection:
    def test_invalid_code_prefix_raises_error(self):
        crawler = DLsiteWorkCrawler(code="XX123456")
        with pytest.raises(ValueError, match="Not Code!"):
            crawler._get_dlsite_url()

    def test_empty_code_raises_error(self):
        crawler = DLsiteWorkCrawler(code="")
        with pytest.raises(ValueError, match="Not Code!"):
            crawler._get_dlsite_url()

    async def test_nonexistent_code_raises_error(self):
        crawler = DLsiteWorkCrawler(code="RJ99999999")
        with pytest.raises(ValueError) as excinfo:
            await crawler.get_use_code()
        assert "Request Fail!!" in str(excinfo.value)
