import os
import shutil
import logging

from os import path as os_path

from dlsite_classification.spkg.logs import Green, Cyan, Red

from .check import check_and_make_folder, check_folder_has_file


def move_subfolder(origin_path, to_path, need_del=False):
    logging.info(f"Move Sub Folder: {origin_path}\tTO\t{to_path}")
    if not os_path.isdir(origin_path):
        return
    check_and_make_folder(to_path)
    for i in os.listdir(origin_path):
        try:
            new_path = os_path.join(to_path, i)
            os.rename(
                os_path.join(origin_path, i),
                new_path
            )
            Green(logging.info, f"Move Sub Folder - Finish {new_path}")
        except BaseException as e:
            Red(logging.error, e)
    if need_del:
        try:
            shutil.rmtree(origin_path)
        except BaseException as e:
            Red(logging.error, e)


def move_folder(root, move_to_folder, origin_folder) -> str:
    logging.info(f"Move Folder: {origin_folder}\tTO\t{move_to_folder}")
    new_root_path = os_path.join(root, move_to_folder)
    check_and_make_folder(new_root_path)
    path = os_path.join(root, origin_folder)
    new_path = os_path.join(new_root_path, origin_folder)
    try:
        os.rename(path, new_path)
        Green(logging.info, f"Move Folder - Finish {new_path}")
        return new_path
    except BaseException as e:
        Red(logging.error, e)
        return ''


def merge_folder_name_move(path: str, name: str, need_del: bool = True) -> str:
    logging.info(f"Merge Folder name: {name}\t+\t{path}")
    origin_path = os_path.join(path, name)
    if path[-1] in ['\\', '/']:
        path = path[:-1]
    new_path = path + name
    try:
        os.rename(origin_path, new_path)
        if need_del:
            os.rmdir(path)
        Green(logging.info, f"Merge Folder - Finish {new_path}")
        return new_path
    except BaseException as e:
        Red(logging.error, e)
        return ''


def extract_folder_top(path: str):
    logging.info(f"Extract Path: {path}")
    hsa_file, white_folder = check_folder_has_file(path)
    if hsa_file:
        Green(logging.info, f"Extract hsa file or No Data - Finish {path}")
        return
    while len(white_folder) != 0:
        folder = white_folder.pop()
        extract_path = os_path.join(path, folder)
        logging.info(f"Extract Path: {extract_path}")
        has_file, temp = check_folder_has_file(
            extract_path
        )
        if has_file or len(temp) == 0:
            Green(logging.info,
                  f"Extract hsa file or No Data - Finish {extract_path}")
            continue
        Cyan(logging.info, f"Extract Folder: {temp}")
        for i in temp:
            new_path = merge_folder_name_move(
                os_path.join(path, folder),
                i,
                False
            )
            if len(new_path) == 0:
                continue
            white_folder.append(new_path)
        else:
            try:
                os.rmdir(os_path.join(path, folder))
            except BaseException as e:
                Red(logging.error, e)
                return
            Green(logging.info, f"Extract Folder - Finish {extract_path}")
