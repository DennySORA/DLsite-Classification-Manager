import logging
import os
from collections import defaultdict
from collections.abc import Iterable
from os import path as os_path

from dlsite_classification.common.regex import REGEX_COMPANY_FOLDER
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Yellow
from dlsite_classification.tools import (
    extract_folder_top,
    move_folder,
    move_subfolder,
    search_file_code,
)

from .folder import Folder


WAIT_FOLDER_NAME = "wait"
IGNORED_ROOT_FOLDERS = {
    "finish",
    "not_classification",
    "look_like_finish",
    "null",
    WAIT_FOLDER_NAME,
}
WAIT_FOLDER_MOVE_TARGETS = {"code", "other"}


def classification_folder(root_path: str) -> list[Folder]:
    Cyan(logging.info, "==========Start Classification Folder==========")
    if not os_path.isdir(root_path):
        Yellow(logging.info, f"Root path does not exist: {root_path}")
        return []

    folders: list[Folder] = []
    folders.extend(_prepare_wait_folders(root_path))
    folders.extend(_collect_root_folders(root_path))
    Blue(logging.info, "==========End Classification Folder==========")
    return folders


def _prepare_wait_folders(root_path: str) -> list[Folder]:
    wait_path = os_path.join(root_path, WAIT_FOLDER_NAME)
    if not os_path.isdir(wait_path):
        Yellow(logging.info, "Not Wait Folder.")
        return []
    folder_names = os.listdir(wait_path)
    _move_special_subfolders(folder_names, wait_path)
    wait_entries = [os_path.join(wait_path, name) for name in os.listdir(wait_path)]
    return _create_folder_objects(wait_entries)


def _move_special_subfolders(folder_names: Iterable[str], origin_path: str) -> None:
    for name in folder_names:
        if name in WAIT_FOLDER_MOVE_TARGETS:
            move_subfolder(os_path.join(origin_path, name), origin_path, True)


def _collect_root_folders(root_path: str) -> list[Folder]:
    folders: list[Folder] = []
    for entry in os.listdir(root_path):
        if entry in IGNORED_ROOT_FOLDERS:
            continue
        if REGEX_COMPANY_FOLDER.match(entry):
            move_folder(root_path, "look_like_finish", entry)
            continue
        moved_path = move_folder(root_path, WAIT_FOLDER_NAME, entry)
        folders.extend(_create_folder_objects([moved_path]))
    return folders


def _create_folder_objects(path_list: Iterable[str]) -> list[Folder]:
    folders: list[Folder] = []
    for folder_path in path_list:
        if not folder_path:
            continue
        Green(logging.info, f"Create Folder Object {folder_path}")
        folders.append(Folder(folder_path))
    return folders


def classification_mode(folders: Iterable[Folder]) -> dict[str, list[Folder]]:
    Cyan(logging.info, "==========Start Classification Mode==========")
    mode_dict: defaultdict[str, list[Folder]] = defaultdict(list)
    for folder in folders:
        if not isinstance(folder, Folder):
            continue
        folder.check_folder_package()
        mode = folder.classification_type()
        mode_dict[mode].append(folder)
    Blue(logging.info, "==========End Classification Mode==========")
    return dict(mode_dict)


def classification_folder_move_top(path: str) -> None:
    Cyan(logging.info, "==========Start Extract Folder==========")
    extract_folder_top(path)
    Blue(logging.info, "==========End Extract Folder==========")

    Cyan(logging.info, "==========Start Search File DLsite Code==========")
    for name in os.listdir(path):
        folder_path = os_path.join(path, name)
        try:
            code = search_file_code(folder_path)
            if code:
                os.rename(folder_path, os_path.join(path, code))
        except Exception as exc:
            logging.warning(f"{folder_path}\n {exc}")
    Blue(logging.info, "==========End Search File DLsite Code==========")
