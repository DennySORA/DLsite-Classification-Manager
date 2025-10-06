import logging
import os
import sys
import time


def InitializeLog(path: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)
    log_file_path = os.path.join(
        path, f"{time.strftime('%Y-%m-%d', time.localtime())}_log.log"
    )

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    stdout_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        handlers=[file_handler, stdout_handler],
        format="【%(levelname)s】 - %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
