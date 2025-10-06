import asyncio
import logging
import re

from bs4 import BeautifulSoup

from dlsite_classification.common.regex import REGEX_RG
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red, Yellow

from .common import CommonCrawler


class DLsiteCompanyCrawler:
    def __init__(self, code=""):
        self.code = code

        self.info = list()

    def _get_text_url_in_a(self, meta: BeautifulSoup) -> tuple[str, str]:
        anchor = getattr(meta, "a", None)
        if anchor is None:
            return "", ""
        text = anchor.text.replace("\n", "")
        href = anchor.get("href") or ""
        return text, href

    def _get_dlsite_company_url(self) -> str:
        return (
            f"https://www.dlsite.com/maniax/circle/profile/=/maker_id/{self.code}.html"
        )

    async def get_company(self):
        Cyan(
            logging.info,
            f"==========Start Crawler DLsite Company {self.code} Code==========",
        )
        url = self._get_dlsite_company_url()
        Green(logging.info, f"Request DLsite Company {self.code} code.")
        _, bs4 = await CommonCrawler.get_request(url)

        # get first page info
        self.info, url = await self.get_first_page_info(bs4, url)
        if len(self.info) == 0:
            Red(
                logging.warning,
                f"==========Crawler DLsite Company {self.code} Fail.==========",
            )
            raise ValueError("Not Data!")

        _, bs4 = await CommonCrawler.get_request(url)
        # get all page info
        temp = bs4.find("td", "page_no").findAll("li")
        if len(temp) == 0:
            temp = [url]
        else:
            temp = [url] + [li.a.get("href") for li in temp[1:-2]]

        all_url_list = temp
        all_url_list = list()
        for i in temp:
            i = i.split("/")
            i.insert(i.index("hd"), "show_type/1")
            all_url_list.append("/".join(i))

        self.info = await self.get_all_page_info(all_url_list, self.info)

        self.code = self.info.get("code", "")
        Blue(
            logging.info,
            f"==========End Crawler DLsite Company {self.code} Code==========",
        )

    async def get_first_page_info(self, bs4, url) -> tuple[dict, str]:
        Cyan(
            logging.info,
            f"==========Start Format Crawler DLsite {self.code} Code==========",
        )
        info = dict()
        # Get title and code
        info["title"] = [
            bs4.find("strong", "prof_maker_name").text.replace("\n", ""),
            url,
        ]
        if info["title"] == "":
            return dict(), ""
        info["code"] = REGEX_RG.findall(url)[0].replace("\n", "")

        # Get 100 page url
        url = bs4.find("div", "display_num_select").findAll("li")[-1].a.get("href")
        return info, url

    async def get_all_page_info(self, url_list: list[str], info: dict) -> dict:
        async def _get_all_page(url: str):
            print(url)
            _, bs4 = await CommonCrawler.get_request(url)
            info.update(await self.format(bs4))

        await asyncio.gather(*[_get_all_page(url) for url in url_list])

        return info

    async def format(self, bs4: BeautifulSoup) -> dict:
        info = dict()
        work_table = bs4.findAll("table", "work_1col_table")[-1].findAll("tr")

        if len(work_table) == 0:
            raise ValueError("Not Data!")

        for work in work_table:
            work_info = dict()

            work_td_0 = work.findAll("td")[0]
            work_td_1 = work.findAll("td")[1]
            work_td_2 = work.findAll("td")[2]

            # Get work title
            work_info["title"] = self._get_text_url_in_a(
                work_td_1.find("dt", "work_name")
            )

            # Get work type
            work_info["type"] = self._get_text_url_in_a(
                work_td_0.find("div", "work_category")
            )

            # Get work date
            work_info["date"] = self._get_text_url_in_a(
                work_td_2.find("li", "sales_date")
            )

            # Get work buy count
            work_info["buy_count"] = work_td_2.find("li", "work_dl clear").text

            # Get work tag
            work_info["tag"] = [
                self._get_text_url_in_a(tag)
                for tag in work_td_1.find("dd", "search_tag").findAll("a")
            ]

            work_info["information"] = work_td_1.find("dd", "work_text").text

            # Get image
            work_info["images"] = await CommonCrawler.get_images(
                [
                    "https:"
                    + work_td_0.find("div", "work_img_popover")
                    .img.get(":src")
                    .split("'")[1]
                ]
            )

            info[work_info["title"][0]] = work_info

        return info

    def get_info(self):
        if len(self.info) != 0:
            return self.info
        return None

    # New methods for efficient work ID extraction (for ARCHIVE feature)

    def _construct_company_works_url(self, page: int = 1) -> str:
        """Construct company works listing URL with pagination.

        Args:
            page: Page number (1-indexed)

        Returns:
            URL for the company works page
        """
        base_url = (
            f"https://www.dlsite.com/maniax/circle/profile/="
            f"/order%5B0%5D/release_d"
            f"/options%5B0%5D/JPN"
            f"/options%5B1%5D/NM"
            f"/per_page/100"
            f"/show_type/1"
            f"/hd/1"
            f"/lang_options%5B0%5D/%E6%97%A5%E6%9C%AC%E8%AA%9E"
            f"/lang_options%5B1%5D/%E8%A8%80%E8%AA%9E%E4%B8%8D%E8%A6%81"
            f"/page/{page}"
            f"/maker_id/{self.code}.html"
        )
        return base_url

    async def _fetch_page_with_retry(
        self, page: int, retry_count: int = 0, max_retries: int = 3
    ) -> tuple[str, BeautifulSoup]:
        """Fetch a page with exponential backoff retry.

        Args:
            page: Page number to fetch
            retry_count: Current retry attempt number
            max_retries: Maximum number of retry attempts

        Returns:
            Tuple of (html, BeautifulSoup object)

        Raises:
            ValueError: If all retry attempts fail
        """
        url = self._construct_company_works_url(page)
        try:
            Green(logging.info, f"Fetching company {self.code} page {page}")
            html, bs4 = await CommonCrawler.get_request(url)
            return html, bs4
        except Exception as e:
            if retry_count < max_retries:
                wait_time = (2**retry_count) * 2
                Red(
                    logging.warning,
                    f"Fetch failed for page {page}, retry {retry_count + 1}/"
                    f"{max_retries} after {wait_time}s: {e}",
                )
                await asyncio.sleep(wait_time)
                return await self._fetch_page_with_retry(page, retry_count + 1)
            else:
                Red(logging.error, f"Failed after {max_retries} retries: {e}")
                raise

    def _extract_work_ids_from_page(self, bs4: BeautifulSoup) -> list[str]:
        """Extract all work IDs from a single page.

        Only extracts work IDs from the main work table (work_1col_table),
        not from recommendations, ads, or other sections on the page.

        Args:
            bs4: BeautifulSoup object of the page

        Returns:
            List of unique work IDs found on the page
        """
        work_ids = []

        # Find work table - only extract IDs from actual work listings
        work_tables = bs4.find_all("table", "work_1col_table")
        if not work_tables:
            Yellow(
                logging.warning,
                f"No work table found on page for company {self.code}",
            )
            return work_ids

        # Use the last table which typically contains the work list
        work_table = work_tables[-1]

        # Find all rows with data-product_id within the work table
        elements = work_table.find_all(attrs={"data-product_id": True})

        for elem in elements:
            work_id = elem.get("data-product_id")
            if (
                work_id
                and work_id not in work_ids
                and re.match(r"^[RBV][JE]\d+$", work_id)
            ):
                work_ids.append(work_id)

        return work_ids

    def _extract_total_work_count(self, bs4: BeautifulSoup) -> int | None:
        """Extract total work count from pagination info.

        Args:
            bs4: BeautifulSoup object of the page

        Returns:
            Total work count, or None if not found
        """
        page_total = bs4.find("div", class_="page_total")
        if page_total:
            text = page_total.get_text()
            match = re.search(r"(\d+)件中", text)
            if match:
                return int(match.group(1))
        return None

    async def get_all_work_ids(self, rate_limit_delay: float = 2.0) -> list[str]:
        """Efficiently crawl all pages to get just work IDs.

        This method is optimized for the ARCHIVE feature where we only need
        work IDs, not full work details.

        Args:
            rate_limit_delay: Delay between page requests in seconds

        Returns:
            List of all unique work IDs for this company

        Raises:
            ValueError: If company has no works or crawling fails
        """
        Cyan(
            logging.info,
            f"==========Start Extracting Work IDs for Company {self.code}==========",
        )

        # Fetch first page
        _, bs4 = await self._fetch_page_with_retry(1)

        # Extract work IDs from first page
        all_work_ids = self._extract_work_ids_from_page(bs4)
        if not all_work_ids:
            Red(logging.error, f"No works found for company {self.code}")
            raise ValueError(f"No works found for company {self.code}")

        Green(logging.info, f"Found {len(all_work_ids)} works on page 1")

        # Determine total pages
        total_count = self._extract_total_work_count(bs4)
        if total_count:
            total_pages = (total_count + 99) // 100
            Cyan(
                logging.info,
                f"Company {self.code}: {total_count} total works, {total_pages} pages",
            )

            # Fetch remaining pages
            if total_pages > 1:
                for page in range(2, total_pages + 1):
                    await asyncio.sleep(rate_limit_delay)

                    try:
                        _, bs4 = await self._fetch_page_with_retry(page)
                        page_ids = self._extract_work_ids_from_page(bs4)
                        all_work_ids.extend(page_ids)
                        Green(
                            logging.info,
                            f"Found {len(page_ids)} works on page {page}",
                        )
                    except Exception as e:
                        Yellow(
                            logging.warning,
                            f"Skipping page {page} due to error: {e}",
                        )
        else:
            Yellow(
                logging.warning,
                f"Could not determine total pages for {self.code}",
            )

        # Remove duplicates while preserving order
        unique_ids = list(dict.fromkeys(all_work_ids))

        Blue(
            logging.info,
            f"==========Extracted {len(unique_ids)} unique work IDs for "
            f"company {self.code}==========",
        )

        return unique_ids
