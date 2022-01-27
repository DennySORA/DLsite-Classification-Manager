import logging

from bs4 import BeautifulSoup

from dlsite_classification.common.regex import REGEX_RJ
from dlsite_classification.common.dlsite import RJ_WEBPATH, BJ_WEBPATH, VJ_WEBPATH, GAME_LIST_TYPE
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red, Yellow
from .common import CommonCrawler


class DLsiteWorkCrawler:

    def __init__(self, code='', title=''):
        self.code = code
        self.title = title

        self.html = None
        self.bs4 = None
        self.info = list()

    def _get_dlsite_url(self):
        url = ''
        if self.code[0] == 'R':
            url = f'{RJ_WEBPATH}{self.code}'
        elif self.code[0] == 'B':
            url = f'{BJ_WEBPATH}{self.code}'
        elif self.code[0] == 'V':
            url = f'{VJ_WEBPATH}{self.code}'
        else:
            Red(logging.warning,
                f"==========Crawler DLsite {self.code} Fail.==========")
            raise ValueError('Not Code!')
        return url

    def _get_text_url_in_a(self, meta: BeautifulSoup) -> tuple[str, str]:
        try:
            return [meta.a.text.replace("\n", ""), meta.a.get('href')]
        except:
            return ["", ""]

    def _tag_convert_dict(self, tables: list) -> dict:
        result = dict()
        for tab in tables:
            result[tab.th.text] = tab.td
        return result

    async def get_use_code(self):
        Cyan(logging.info,
             f"==========Start Crawler DLsite {self.code} Code==========")
        url = self._get_dlsite_url()
        Green(logging.info, f"Request DLsite {self.code} code.")
        self.html, self.bs4 = await CommonCrawler.get_request(url)

        # format
        self.info = await self.format(self.bs4, url)
        if len(self.info) == 0:
            Red(logging.warning,
                f"==========Crawler DLsite {self.code} Fail.==========")
            raise ValueError('Not Data!')

        self.code = self.info.get('code', '')
        self.title = self.info.get('title', '')
        Blue(logging.info,
             f"==========End Crawler DLsite {self.code} Code==========")

    async def format(self, bs4, url) -> dict:
        Cyan(logging.info,
             f"==========Start Format Crawler DLsite {self.code} Code==========")
        info = dict()
        # Get title and code
        info['title'] = [bs4.h1.text.replace("\n", ""), url]
        if info['title'] == '':
            return dict()
        info['code'] = REGEX_RJ.findall(url)[0].replace("\n", "")

        # Get company
        metadata = bs4.find(id='work_right_inner')
        info['company'] = self._get_text_url_in_a(
            metadata.find('span', 'maker_name')
        )

        tag_list = metadata.find('table', id='work_outline').findAll('tr')

        # Get all tag
        info.update({
            tag_table.th.text:
                [
                    tag.strip()
                    for tag in tag_table.td.text.split('\n')
                    if tag.strip() != ''
                ]
            for tag_table in tag_list
        })

        info['introduction'] = bs4.find('div', 'work_parts_area').text

        # Get image
        info['images'] = await CommonCrawler.get_images(
            [
                'https:'+i.get('data-src')
                for i in bs4.find('div', 'product-slider-data').findAll('div')
            ]
        )

        Blue(logging.info,
             f"==========End Format Crawler DLsite {self.code} Code==========")
        return info

    def get_info(self):
        if len(self.info) != 0:
            return self.info
        else:
            return None
