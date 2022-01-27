
import os
import logging

from dlsite_classification.compare.folder_compare import FolderCompare
from dlsite_classification.compare.file_compare import FileCompare

async def compare_file_hash_func():
    logging.info("Start compare file hash.")
    while True:
        path = input("Please input path:")
        if os.path.isdir(path):
            break

    compare = FileCompare(path)
    await compare.compare()


async def compare_folder_name_func():
    logging.info("Start compare folder name.")
    while True:
        origin_path = input("Please input origin path:")
        compare_path = input("Please input compare path:")
        if all([
            os.path.isdir(origin_path),
            os.path.isdir(compare_path)
        ]):
            break

    compare = FolderCompare(origin_path, compare_path)
    compare.compare()
