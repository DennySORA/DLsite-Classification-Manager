import logging
import os
from os import path as os_path

from dlsite_classification.spkg.logs import Cyan, Green, Red, Yellow


def check_and_make_folder(path: str) -> None:
    if not os_path.isdir(path):
        Cyan(logging.info, f"Make Folder {path}")
        try:
            os.makedirs(path)
        except OSError as exc:
            Red(logging.error, str(exc))


def check_folder_has_file(path: str) -> tuple[bool, list[str]]:
    Cyan(logging.info, f"Check Folder Has File In {path}")
    dir_list = os.listdir(path)
    for name in dir_list:
        if os_path.isfile(os_path.join(path, name)):
            Green(logging.info, f"Has File in {path}")
            return True, dir_list
    Yellow(logging.info, f"No File in {path}")
    return False, dir_list
