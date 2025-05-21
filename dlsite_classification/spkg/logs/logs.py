# -*- coding: utf-8 -*-
import os
import sys
import time
import logging


def InitializeLog(path: str):
    if not os.path.isdir(path):
        os.mkdir(path)
    logFile = open(
        f"{path}/{time.strftime('%Y-%m-%d', time.localtime())}_log.log", "a", encoding="utf-8")

    file_handler = logging.StreamHandler(logFile)
    stdout_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        handlers=[file_handler, stdout_handler],
        format="【%(levelname)s】 - %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
