from sqlite3 import Timestamp
import time
import urllib.parse

from .common import CommonCrawler

class DLsiteSuggestCrawler:

    def __init__(self, title=''):
        self.title = title
        self.suggest_list:dict = dict()

    async def get_suggest(self):
        timestamp = str(int(time.time()*1000))
        work_url = urllib.parse.quote_plus(self.title)
        result = await CommonCrawler.get_request(f"https://www.dlsite.com/suggest/?term={work_url}&site=adult-jp&time={timestamp}",is_json=True)
        if isinstance(result,dict):
            self.suggest_list = result
