import logging
import asyncio

from bs4 import BeautifulSoup

from dlsite_classification.common.regex import REGEX_RG
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red
from .common import CommonCrawler


class DLsiteCompanyCrawler:

    def __init__(self, code=''):
        self.code = code

        self.info = list()

    def _get_text_url_in_a(self, meta: BeautifulSoup) -> tuple[str, str]:
        try:
            return [meta.a.text.replace("\n", ""), meta.a.get('href')]
        except:
            return ["", ""]

    def _get_dlsite_company_url(self) -> str:
        return f"https://www.dlsite.com/maniax/circle/profile/=/maker_id/{self.code}.html"

    async def get_company(self):
        Cyan(logging.info,
             f"==========Start Crawler DLsite Company {self.code} Code==========")
        url = self._get_dlsite_company_url()
        Green(logging.info, f"Request DLsite Company {self.code} code.")
        _, bs4 = await CommonCrawler.get_request(url)

        # get first page info
        self.info, url = await self.get_first_page_info(bs4, url)
        if len(self.info) == 0:
            Red(logging.warning,
                f"==========Crawler DLsite Company {self.code} Fail.==========")
            raise ValueError('Not Data!')

        _, bs4 = await CommonCrawler.get_request(url)
        # get all page info
        temp = bs4.find('td', 'page_no').findAll('li')
        if len(temp) == 0:
            temp = [url]
        else:
            temp = [url] + [li.a.get('href')
                            for li in temp[1:-2]]

        all_url_list = temp
        all_url_list = list()
        for i in temp:
            i = i.split('/')
            i.insert(i.index('hd'), 'show_type/1')
            all_url_list.append('/'.join(i))

        self.info = await self.get_all_page_info(all_url_list, self.info)

        self.code = self.info.get('code', '')
        Blue(logging.info,
             f"==========End Crawler DLsite Company {self.code} Code==========")

    async def get_first_page_info(self, bs4, url) -> tuple[dict, str]:
        Cyan(logging.info,
             f"==========Start Format Crawler DLsite {self.code} Code==========")
        info = dict()
        # Get title and code
        info['title'] = [
            bs4.find('strong', 'prof_maker_name').text.replace("\n", ""), url]
        if info['title'] == '':
            return dict(), ''
        info['code'] = REGEX_RG.findall(url)[0].replace("\n", "")

        # Get 100 page url
        url = bs4.find('div', 'display_num_select').findAll(
            'li')[-1].a.get('href')
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
        work_table = bs4.findAll('table', 'work_1col_table')[-1].findAll('tr')

        if len(work_table) == 0:
            raise ValueError('Not Data!')

        for work in work_table:
            work_info = dict()

            work_td_0 = work.findAll('td')[0]
            work_td_1 = work.findAll('td')[1]
            work_td_2 = work.findAll('td')[2]

            # Get work title
            work_info['title'] = self._get_text_url_in_a(
                work_td_1.find('dt', 'work_name'))

            # Get work type
            work_info['type'] = self._get_text_url_in_a(
                work_td_0.find('div', 'work_category'))

            # Get work date
            work_info['date'] = self._get_text_url_in_a(
                work_td_2.find('li', 'sales_date'))

            # Get work buy count
            work_info['buy_count'] = work_td_2.find('li', 'work_dl clear').text

            # Get work tag
            work_info['tag'] = [
                self._get_text_url_in_a(tag)
                for tag in work_td_1.find('dd', 'search_tag').findAll('a')
            ]

            work_info['information'] = work_td_1.find('dd', 'work_text').text

            # Get image
            work_info['images'] = await CommonCrawler.get_images(
                [
                    'https:' +
                    work_td_0.find(
                        'div', 'work_img_popover'
                    ).img.get(':src').split('\'')[1]
                ]
            )

            info[work_info['title'][0]] = work_info

        return info

    def get_info(self):
        if len(self.info) != 0:
            return self.info
        else:
            return None
