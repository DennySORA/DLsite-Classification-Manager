import hashlib
import json
import logging
import os
from collections.abc import Awaitable, Callable, Iterator
from typing import Any

from aiofile import async_open

from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red, Yellow
from dlsite_classification.spkg.sasync.running import SAsyncRunner
from dlsite_classification.tools.scan import get_folder_cla_struct


BUF_SIZE = 65536
FileEntry = tuple[str, str]
HashRecord = tuple[str, str, int]
HashBox = dict[str, list[HashRecord]]
AsyncTask = Callable[[], Awaitable[None]]
DuplicateRecord = tuple[str, list[str], HashBox]
OkRecord = tuple[str, HashBox]


class FileCompare:
    def __init__(self, path: str):
        self.root_path: str = path
        self.folder_box: dict[str, dict[str, str]] = {}
        self.compare_count: int = 0
        self.duplicate_records: list[DuplicateRecord] = []
        self.ok_records: list[OkRecord] = []
        self.folder_file_hash_box: dict[str, list[Any]] = {
            "duplicate": self.duplicate_records,
            "ok": self.ok_records,
        }
        self.need_check_file: list[tuple[list[FileEntry], str]] = []

    @staticmethod
    async def hash_file(path: str) -> str:
        sha256 = hashlib.sha256()
        async with async_open(path, "rb") as afp:
            while True:
                data = await afp.read(BUF_SIZE)
                if not data or not isinstance(data, bytes):
                    break
                sha256.update(data)
        return sha256.hexdigest()

    @staticmethod
    def _get_file_list(path: str) -> list[FileEntry]:
        return [
            (file, os.path.join(root, file))
            for root, _, files in os.walk(path)
            for file in files
        ]

    def _get_work_path(self) -> Iterator[tuple[str, str]]:
        for company, val in self.folder_box.items():
            for work, path in val.items():
                yield f"{company}|{work}", path

    async def hash_work(self, file_list: list[FileEntry]) -> tuple[list[str], HashBox]:
        hash_box: HashBox = {}
        duplicate: set[str] = set()
        for file_name, file_path in file_list:
            print(
                f"Need to Work task {self.compare_count}........", flush=True, end="\r"
            )
            hash_id = await self.hash_file(file_path)
            self.compare_count -= 1
            print(
                f"Need to Work task {self.compare_count}........", flush=True, end="\r"
            )
            size = os.path.getsize(file_path)
            if hash_box.get(hash_id) is None:
                hash_box[hash_id] = [(file_name, file_path, size)]
                continue
            duplicate.add(hash_id)
            hash_box[hash_id].append((file_name, file_path, size))
        return list(duplicate), hash_box

    async def check_duplicate(self, file_list: list[FileEntry], name: str) -> None:
        Cyan(logging.info, f"Start Compare Work {name}")
        duplicate, hash_box = await self.hash_work(file_list)
        if len(duplicate) == 0:
            Blue(logging.info, f"{name} Compare Finish is Not Duplicate file.")
            self.ok_records.append((name, hash_box))
            return
        Yellow(logging.info, f"{name} Compare Finish has Duplicate File.")
        self.duplicate_records.append((name, duplicate, hash_box))

    def _wrap(self, file_list: list[FileEntry], name: str) -> AsyncTask:
        async def doing() -> None:
            try:
                await self.check_duplicate(file_list, name)
            except BaseException as e:
                Red(logging.error, str(e))

        return doing

    async def compare(self) -> None:
        self.folder_box = get_folder_cla_struct(self.root_path)

        for name, path in self._get_work_path():
            file_list = self._get_file_list(path)
            self.compare_count += len(file_list)
            print(f"Find file total: {self.compare_count}", end="\r", flush=True)
            self.need_check_file.append((file_list, name))

        await self._task_pool()
        self.save_report()

    def save_report(self) -> None:
        result_duplicate: list[dict[str, Any]] = []
        for name, duplicate_hash_ids, hash_box in self.duplicate_records:
            duplicate_file_list: list[list[HashRecord]] = [
                hash_box[hash_id]
                for hash_id in duplicate_hash_ids
                if hash_id in hash_box
            ]
            duplicate_file_list.sort(key=lambda records: records[0][2], reverse=True)
            duplicate_size_mb = (
                sum(
                    sum(file_data[2] for file_data in records[1:])
                    for records in duplicate_file_list
                    if len(records) > 1
                )
                / 1024
                / 1024
            )
            result_duplicate.append(
                {
                    "name": name,
                    "duplicate_file_size": duplicate_size_mb,
                    "duplicate_hash_id": duplicate_hash_ids,
                    "duplicate_file_list": duplicate_file_list,
                }
            )
        result_duplicate.sort(key=lambda x: x["duplicate_file_size"], reverse=True)
        with open("duplicate.json", "w", encoding="utf-8") as fp:
            json.dump(result_duplicate, fp, ensure_ascii=False)

    async def _task_pool(self) -> None:
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
        need_run_func_count = min(need_run_func_count, 10)
        await sasync.run(need_run_func_count)
