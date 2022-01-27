
import os
import json
import logging
import hashlib

from aiofile import async_open
from typing import Iterator

from dlsite_classification.tools.scan import get_folder_cla_struct
from dlsite_classification.spkg.sasync.running import SAsyncRunner
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red, Yellow

BUF_SIZE = 65536


class FileCompare:

    def __init__(self, path: str):
        self.root_path: str = path
        self.folder_box: dict[str, dict[str, str]] = dict()
        self.compare_count: int = 0
        self.folder_file_hash_box: dict[str, list] = {
            "duplicate": [], "ok": []}
        self.need_check_file: list[tuple[list[tuple[str, str]], str]] = []

    @staticmethod
    async def hash_file(path) -> str:
        sha1 = hashlib.sha1()
        async with async_open(path, 'rb') as afp:
            while True:
                data = await afp.read(BUF_SIZE)
                if not data or not isinstance(data, bytes):
                    break
                sha1.update(data)
        return sha1.hexdigest()

    @staticmethod
    def _get_file_list(path: str) -> list[tuple[str, str]]:
        return [
            (file, os.path.join(root, file))
            for root, _, files in os.walk(path)
            for file in files
        ]

    def _get_work_path(self) -> Iterator[tuple[str, str]]:
        for company, val in self.folder_box.items():
            for work, path in val.items():
                yield f"{company}|{work}", path

    async def hash_work(self, file_list: list[tuple[str, str]]) -> tuple[list[str], dict[str, list[tuple[str, str, int]]]]:
        hash_box: dict[str, list[tuple[str, str, int]]] = dict()
        duplicate: set[str] = set()
        for file_name, file_path in file_list:
            print(f"Need to Work task {self.compare_count}........",
                  flush=True, end="\r")
            hash_id = await self.hash_file(file_path)
            self.compare_count -= 1
            print(f"Need to Work task {self.compare_count}........",
                  flush=True, end="\r")
            size = os.path.getsize(file_path)
            if hash_box.get(hash_id, None) is None:
                hash_box[hash_id] = [(file_name, file_path, size)]
                continue
            duplicate.add(hash_id)
            hash_box[hash_id].append((file_name, file_path, size))
        return list(duplicate), hash_box

    async def check_duplicate(self, file_list: list[tuple[str, str]], name: str):
        Cyan(logging.info, f"Start Compare Work {name}")
        duplicate, hash_box = await self.hash_work(file_list)
        if len(duplicate) == 0:
            Blue(logging.info, f"{name} Compare Finish is Not Duplicate file.")
            self.folder_file_hash_box["ok"].append((name, hash_box))
            return
        Yellow(logging.info, f"{name} Compare Finish has Duplicate File.")
        self.folder_file_hash_box["duplicate"].append(
            (name, duplicate, hash_box))

    def _wrap(self, file_list: list[tuple[str, str]], name: str):
        async def doing():
            try:
                await self.check_duplicate(file_list, name)
            except BaseException as e:
                Red(logging.error, e)
        return doing

    async def compare(self):
        self.folder_box = get_folder_cla_struct(self.root_path)

        for name, path in self._get_work_path():
            file_list = self._get_file_list(path)
            self.compare_count += len(file_list)
            print(f"Find file total: {self.compare_count}",
                  end="\r", flush=True)
            self.need_check_file.append((file_list, name))

        await self._task_pool()
        self.save_report()

    def save_report(self):
        result_duplicate = list()
        for i in self.folder_file_hash_box["duplicate"]:
            hash_box = i[2]
            duplicate_file_list = [hash_box.get(j) for j in i[1]]
            duplicate_file_list.sort(key=lambda x: x[0][2], reverse=True)
            result_duplicate.append(
                {
                    "name": i[0],
                    "duplicate_file_size": sum([sum([j[2] for j in i[1:]]) for i in duplicate_file_list])/1024/1024,
                    "duplicate_hash_id": i[1],
                    "duplicate_file_list": duplicate_file_list,
                }
            )
        result_duplicate.sort(
            key=lambda x: x["duplicate_file_size"], reverse=True)
        with open("duplicate.json", "w", encoding="utf-8") as fp:
            json.dump(result_duplicate, fp, ensure_ascii=False)

    async def _task_pool(self):
        Cyan(logging.info, f"Need to Work compare file {self.compare_count}")

        sasync = SAsyncRunner()
        read_queue = sasync.get_read_queue()

        # Create async runner
        Cyan(logging.info, "==========Start Create Compare Task ==========")
        # create crawler and injection to file class
        for file_list, name in self.need_check_file:
            await read_queue.put(self._wrap(file_list, name))
            Green(logging.info, f"Create {name} Compare.")
        Blue(logging.info, "==========End Create Compare Task==========")

        need_run_func_count = read_queue.qsize()
        if need_run_func_count > 10:
            need_run_func_count = 10
        await sasync.run(need_run_func_count)
