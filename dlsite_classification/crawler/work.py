import logging
from typing import Any

from bs4 import BeautifulSoup
from bs4.element import Tag

from dlsite_classification.common.dlsite import BJ_WEBPATH, RJ_WEBPATH, VJ_WEBPATH
from dlsite_classification.common.regex import REGEX_RJ
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red

from .common import CommonCrawler


class DLsiteWorkCrawler:
    def __init__(self, code: str = "", title: str = "") -> None:
        self.code = code
        self.title = title

        self.html: str | None = None
        self.bs4: BeautifulSoup | None = None
        self.info: dict[str, Any] = {}

    def _get_dlsite_url(self) -> str:
        code = (self.code or "").strip().upper()
        if not code:
            Red(logging.warning, "==========Crawler DLsite Empty Code Fail.==========")
            raise ValueError("Not Code!")

        prefix_map = {
            "R": RJ_WEBPATH,
            "B": BJ_WEBPATH,
            "V": VJ_WEBPATH,
        }

        base = prefix_map.get(code[0])
        if base is None:
            Red(
                logging.warning,
                f"==========Crawler DLsite {code} Invalid Prefix Fail.==========",
            )
            raise ValueError("Not Code!")

        self.code = code
        return f"{base}{code}"

    def _get_text_url_in_a(self, meta: Tag | None) -> list[str]:
        if meta is None:
            return ["", ""]

        anchor = meta.find("a")
        if anchor is None:
            return ["", ""]

        text = anchor.text.replace("\n", "")
        href = anchor.get("href") or ""
        return [text, href]

    def _tag_convert_dict(self, tables: list[Tag]) -> dict[str, Tag]:
        result: dict[str, Tag] = {}
        for tab in tables:
            result[tab.th.text] = tab.td
        return result

    async def get_use_code(self) -> None:
        Cyan(logging.info, f"==========Start Crawler DLsite {self.code} Code==========")
        url = self._get_dlsite_url()
        Green(logging.info, f"Request DLsite {self.code} code.")
        self.html, self.bs4 = await CommonCrawler.get_request(url)

        # format
        self.info = await self.format(self.bs4, url)
        if len(self.info) == 0:
            Red(
                logging.warning, f"==========Crawler DLsite {self.code} Fail.=========="
            )
            raise ValueError("Not Data!")

        self.code = self.info.get("code", "")
        self.title = self.info.get("title", "")
        Blue(logging.info, f"==========End Crawler DLsite {self.code} Code==========")

    async def format(self, bs4: BeautifulSoup | None, url: str) -> dict[str, Any]:
        Cyan(
            logging.info,
            f"==========Start Format Crawler DLsite {self.code} Code==========",
        )
        info: dict[str, Any] = {}
        # Get title and code
        if bs4 is None:
            raise ValueError("Empty response body")

        title_tag = bs4.find("h1")
        if title_tag is None:
            raise ValueError("DLsite page format changed: missing <h1> tag")

        title_text = title_tag.text.replace("\n", "")
        if title_text == "":
            raise ValueError("DLsite page format changed: empty title")

        info["title"] = [title_text, url]

        matched_codes = REGEX_RJ.findall(url)
        if not matched_codes:
            raise ValueError("DLsite page format changed: code not found in URL")
        info["code"] = matched_codes[0].replace("\n", "")

        # Get company
        metadata = bs4.find(id="work_right_inner")
        if metadata is None:
            raise ValueError(
                "DLsite page format changed: missing #work_right_inner container"
            )

        company_meta = metadata.find("span", "maker_name")
        info["company"] = self._get_text_url_in_a(company_meta)

        outline_table = metadata.find("table", id="work_outline")
        if outline_table is None:
            raise ValueError("DLsite page format changed: missing table#work_outline")

        tag_list = outline_table.find_all("tr")

        # Get all tag
        info.update(
            {
                tag_table.th.text: [
                    tag.strip()
                    for tag in tag_table.td.text.split()
                    if tag.strip() != ""
                ]
                for tag_table in tag_list
            }
        )

        intro = bs4.find("div", "work_parts_area")
        if intro is None:
            raise ValueError("DLsite page format changed: missing div.work_parts_area")
        info["introduction"] = intro.text

        # Get image
        slider = bs4.find("div", "product-slider-data")
        if slider is None:
            raise ValueError(
                "DLsite page format changed: missing div.product-slider-data"
            )

        image_divs = slider.find_all("div")
        image_urls = []
        for div in image_divs:
            data_src = div.get("data-src")
            if data_src:
                image_urls.append("https:" + data_src)

        if not image_urls:
            raise ValueError("DLsite page format changed: no image data-src found")

        info["images"] = await CommonCrawler.get_images(image_urls)

        Blue(
            logging.info,
            f"==========End Format Crawler DLsite {self.code} Code==========",
        )
        return info

    def get_info(self) -> dict[str, Any] | None:
        if len(self.info) != 0:
            return self.info
        return None
