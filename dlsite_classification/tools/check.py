import os
import logging

from os import path as os_path
from dlsite_classification.spkg.logs import Green, Cyan, Red, Yellow


def check_and_make_folder(path):
    if not os_path.isdir(path):
        Cyan(logging.info, f"Make Folder {path}")
        try:
            os.makedirs(path)
        except BaseException as e:
            Red(logging.error, e)


def check_folder_has_file(path) -> tuple:
    Cyan(logging.info, f"Check Folder Has File In {path}")
    dir_list = os.listdir(path)
    for i in dir_list:
        if os_path.isfile(os_path.join(path, i)):
            Green(logging.info, f"Has File in {path}")
            return True, dir_list
    Yellow(logging.info, f"No File in {path}")
    return False, dir_list
