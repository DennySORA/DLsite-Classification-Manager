import os
import logging

from os import path as os_path

from dlsite_classification.tools import move_subfolder, move_folder, search_file_code, extract_folder_top
from dlsite_classification.common.regex import REGEX_COMPANY_FOLDER
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Yellow

from .folder import Folder


def classification_folder(root_path: str) -> list:
    need_classification_folder = list()
    Cyan(logging.info, "==========Start Classification Folder==========")

    def create_folder_obj(path_list: list):
        for path in path_list:
            if len(path) == 0:
                continue
            Green(logging.info, f"Create Folder Object {path}")
            need_classification_folder.append(Folder(path))

    def check_in_move(check, check_point, origin_path):
        for i in check:
            if i in check_point:
                move_subfolder(
                    os_path.join(origin_path, i),
                    origin_path,
                    True
                )

    def check_wait():
        wait_path = os_path.join(root_path, 'wait')
        if not os_path.isdir(wait_path):
            Yellow(logging.info, "Not Wait Folder.")
            return
        folder_content = os.listdir(wait_path)
        check_in_move(folder_content, ['code', 'other'], wait_path)
        create_folder_obj(
            [
                os_path.join(wait_path, i)
                for i in os.listdir(wait_path)
            ]
        )

    root_folder = os.listdir(root_path)
    if len(root_folder) == 0:
        return []

    check_wait()

    for i in root_folder:
        if i in [
            'finish', 'not_classification',
            'look_like_finish', 'null', 'wait'
        ]:
            continue
        elif REGEX_COMPANY_FOLDER.match(i):
            move_folder(root_path, 'look_like_finish', i)
        else:
            create_folder_obj(
                [move_folder(root_path, 'wait', i)]
            )
    Blue(logging.info, "==========End Classification Folder==========")
    return need_classification_folder


def classification_mode(folders: list):
    Cyan(logging.info, "==========Start Classification Mode==========")
    mode_dict = {}
    for i in folders:
        if not isinstance(i, Folder):
            continue
        i.check_folder_package()
        mode = i.classification_type()
        try:
            mode_dict[mode].append(i)
        except:
            mode_dict[mode] = [i]
    Blue(logging.info, "==========End Classification Mode==========")
    return mode_dict


def classification_folder_move_top(path: str):
    Cyan(logging.info, "==========Start Extract Folder==========")
    extract_folder_top(path)
    Blue(logging.info, "==========End Extract Folder==========")

    Cyan(logging.info, "==========Start Search File DLsite Code==========")
    for i in os.listdir(path):
        folder_path = os_path.join(path, i)
        try:
            code = search_file_code(folder_path)
            if code != None and len(code) != 0:
                os.rename(folder_path, os_path.join(path, code))
        except BaseException as e:
            logging.warning(f"{folder_path}\n {e}")
    Blue(logging.info, "==========End Search File DLsite Code==========")
