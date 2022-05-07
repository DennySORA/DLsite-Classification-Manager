
import os
import time
import asyncio
import logging

from itertools import islice
from collections import OrderedDict

from dlsite_classification.tools import raed_data
from dlsite_classification.common.regex import REGEX_COMPANY_FOLDER, REGEX_RJ
from dlsite_classification.spkg.logs import Green, Cyan
from dlsite_classification.spkg.sasync import SAsyncRunner

from .structure import Company, Work, WorkInfo, Tag, conversion_table


class ExtractFolder:

    def __init__(self, path: str):
        self.classification_table: OrderedDict[str, Company] = OrderedDict()
        self.path = path
        self.scan_count = 0

    def _work_count(self):
        print(f"Extracting work : {self.scan_count}", end="\r", flush=True)

    async def make_tag(self, tags_table: dict[str, str]) -> Tag:
        temp = dict()

        async def _load(name, val):
            self.scan_count += 1
            self._work_count()
            eng_name = conversion_table.get(name)
            data = (await raed_data(val)).split('\n')
            if eng_name in ["company", 'title']:
                temp[eng_name] = {data[0]: data[1]}
            elif eng_name in ["introduction", "code","request_failed"]:
                temp[eng_name] = "\n".join(data)
            elif eng_name in ["star"]:
                temp[eng_name] = (
                    int(data[0]),
                    data[1] if len(data) == 2 else ""
                )
            else:
                temp[eng_name] = {i: True for i in data}
            self.scan_count -= 1
            self._work_count()

        await asyncio.gather(
            *[
                _load(name, val)
                for name, val in tags_table.items()
            ]
        )
        return Tag(**temp)

    def get_all_table(self) -> OrderedDict[str, Company]:
        return self.classification_table

    def get_table(self, limit=100, offset=0) -> list:
        return list(
            islice(
                self.classification_table.items(),
                offset,
                offset+limit
            ),
        )

    async def _scan(self, origin_folder_path):
        if not REGEX_COMPANY_FOLDER.match(origin_folder_path):
            return
        company_folder_path = os.path.join(
            self.path,
            origin_folder_path
        )
        Cyan(logging.info, f"Extracting {origin_folder_path}")
        work_item = await self.scan_company(company_folder_path)
        self.classification_table[origin_folder_path] = Company(
            name=origin_folder_path,
            path=company_folder_path,
            work_item=work_item
        )
        Green(logging.info, f"Extract Finish {origin_folder_path}")

    def _scan_wrap(self, origin_folder_path):
        async def doing():
            await self._scan(origin_folder_path)
        return doing

    async def scan_file(self):
        start_time = time.time()
        sasync = SAsyncRunner()
        read_queue = sasync.get_read_queue()
        for origin_folder_path in os.listdir(self.path):
            await read_queue.put(
                self._scan_wrap(origin_folder_path)
            )
        run_limit = read_queue.qsize()
        if run_limit > 30:
            run_limit = 30
        await sasync.run(run_limit)
        return time.time() - start_time

    async def scan_company(self, path: str) -> dict[str, dict]:
        result = dict()
        for work_folder in os.listdir(path):
            code = REGEX_RJ.findall(work_folder)
            name = work_folder.split("] ")[-1]
            if len(code) == 0:
                continue
            code = code[0]
            work_folder_path = os.path.join(path, work_folder)
            try:
                info_data = await self.scan_work(work_folder_path, code)
            except:
                info_data = None
            result[work_folder] = Work(
                name=name,
                path=work_folder_path,
                code=code,
                info=info_data
            )
        return result

    async def scan_work(self, path: str, code: str) -> WorkInfo:
        images = []
        tags = {}
        path = os.path.join(path, f"{code}_info")
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found info data.")
        for i in os.listdir(path):
            temp = i.split('.')
            if temp[-1] == "tag":
                tags[temp[0]] = os.path.join(path, i)
            else:
                images.append(i)
        try:
            tag = await self.make_tag(tags)
        except Exception as e:
            logging.error(f"{path} - Error {e}")
            raise e
        work_info = WorkInfo(
            path=path,
            images=images,
            tag=tag
        )
        return work_info
