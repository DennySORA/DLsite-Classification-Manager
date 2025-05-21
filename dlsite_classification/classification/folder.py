import os
import time
import shutil
import logging
import asyncio

from typing import Optional
from os import path as os_path

from dlsite_classification.tools import check_and_make_folder, save_data, replace_file_name, check_folder_has_file, merge_folder_name_move
from dlsite_classification.common.regex import REGEX_RJ, REGEX_RG
from dlsite_classification.spkg.logs import Blue, Cyan, Yellow, Red


class Folder:

    def __init__(self, path: str):
        self._get_path(path)

        self.file_info = dict()
        self.crawler = None

    def _get_path(self, path: str):
        Cyan(logging.info, f"Update Folder Path {path}")

        self.path = path

        path_temp = os_path.split(path)
        self.root_path = str(path_temp[0])
        self.folder_name = str(path_temp[1])

    async def _save_tag(self, info_folder_path, name: str, data=[]):

        # Check
        if isinstance(data, tuple):
            data = list(data)
        elif not isinstance(data, list):
            data = [data]
        elif len(data) == 0:
            return

        # replace
        Blue(logging.info, f"Save tag {name} in {self.folder_name}")
        file_name = replace_file_name(f'{name}.tag')
        file_path = os_path.join(info_folder_path, file_name)
        await save_data(file_path, '\n'.join(data))

    async def _save_images(self, path: str, images: Optional[list] = None):
        if images is None:
            images = self.file_info.get('images', None)
        if images is None:
            return
        Blue(logging.info, f"Save {self.folder_name} image.")
        await asyncio.gather(
            *[
                save_data(
                    os_path.join(
                        path,
                        i.get('name', ''),
                    ),
                    i.get('data', '')
                ) for i in images
            ]
        )

    def _get_rename(self, code: str, is_company: bool = False) -> str:

        # Get Title and company
        title = self.file_info.get('title', list())[0]
        company = self.file_info.get('company', list())
        company_name = company[0]
        company_code_name = REGEX_RG.findall(company[1])[0].replace("\n", "")

        if is_company:
            return os_path.join(
                os_path.split(self.root_path)[0],
                replace_file_name(
                    f'[{company_name}]_[{company_code_name}]'
                )
            )
        else:
            return os_path.join(
                self.root_path,
                replace_file_name(
                    f'[{code}]_[{company_name}]_[{company_code_name}] {title}'
                )
            )

    # ---------------------------------------
    # ---------------------------------------
    # ---------------------------------------

    def use_crawler(self, crawler):
        self.crawler = crawler

    def move_to(self, folder_name, new_name=None):

        code_path = os_path.join(self.root_path, folder_name)
        Cyan(logging.info,
             f"Move Folder {self.root_path} TO {code_path} - {new_name}")

        # check folder is existed.
        check_and_make_folder(code_path)

        # Move file.
        if new_name == None:
            new_name = self.folder_name
        new_path = os_path.join(code_path, new_name)

        if os_path.isdir(new_path):
            duplicate_path = os_path.join(
                self.root_path,
                "duplicate"
            )
            check_and_make_folder(duplicate_path)
            new_path = os_path.join(
                duplicate_path,
                f"{new_name}_{time.time()}"
            )

        try:
            file = open(os_path.join(
                self.path,
                ".dlsite_classification.path.old"
            ), "a+", encoding="utf-8")
            file.write(self.path+"\n")
            file.write(new_path+"\n")
            file.close()
            os.rename(self.path, new_path)
        except BaseException as e:
            Red(logging.error, e)
            return

        # Update name and path.
        self._get_path(new_path)

    # ---------------------------------------
    # ---------------------------------------
    # ---------------------------------------

    def check_folder_package(self):
        Cyan(logging.info,
             f"==========Start Check Folder Recursive in {self.path}==========")

        has_file, data = check_folder_has_file(self.path)
        data_count = len(data)
        if data_count > 1 or has_file:
            Cyan(
                logging.info, f"==========End Check Folder Recursive because Has Data in {self.path}==========")
            return
        elif data_count == 0:
            self.move_to('null')
            Cyan(
                logging.info, f"==========End Check Folder Recursive because Null in {self.path}==========")
            return
        elif data_count == 1:
            new_path = merge_folder_name_move(self.path, data[0])
            if len(new_path) == 0:
                return
            self._get_path(new_path)
            self.check_folder_package()

    def classification_type(self, is_move=True):
        Cyan(logging.info, f"Get {self.folder_name} Code in {self.path}")
        code = REGEX_RJ.findall(self.folder_name)
        if len(code) != 0:
            if is_move:
                self.move_to('code', code[0])
            self.file_info['code'] = str(code[0])
            return 'code'
        else:
            if is_move:
                self.move_to('other')
            return 'other'
    
    async def set_request_failed(self):
        if self.crawler is None:
            raise Exception("Not use crawler.")
        code = self.crawler.code
        info_folder_path = os_path.join(self.path, code+'_info')
        await self._save_tag(
            info_folder_path, 
            f'request_failed', 
            f'Request Failed :{time.time()}'
        )

    def get_info(self) -> bool:
        if self.crawler is None:
            raise Exception("Not use crawler.")
        self.file_info = self.crawler.get_info()
        if self.file_info is None:
            return False
        return True

    async def classify(self, is_move=True):
        Cyan(logging.info,
             f"==========Start Classify Folder in {self.path}==========")
        # Create info folder
        code = self.file_info.get('code', '')
        info_folder_path = os_path.join(self.path, code+'_info')
        if os_path.isdir(info_folder_path):
            shutil.rmtree(info_folder_path)
        check_and_make_folder(info_folder_path)

        # Save data
        await asyncio.gather(
            self._save_images(info_folder_path),
            *[
                self._save_tag(info_folder_path, key, val)
                for key, val in self.file_info.items() if key != 'images'
            ]
        )
        
        if is_move:
            # Move folder
            self.move_to(self.path, self._get_rename(code))

        Blue(logging.info,
             f"==========End Classify Folder in {self.path}==========")

    async def rename(self, is_company:bool=False):
        code = self.file_info.get('code', '')

        if is_company:
            path = self._get_rename(code, True)
            if not os_path.exists(path):
                os.rename(self.root_path, path)
        else:
            os.rename(self.path, self._get_rename(code))

    def finish(self):
        Cyan(logging.info,
             f"==========Start Move Finish Folder in {self.path}==========")
        root = os_path.join(self.root_path, '../../finish/')
        company = self.file_info.get('company', list())
        if len(company) == 0:
            Yellow(logging.warning, "Not company in {self.path}")
            return
        company_name = replace_file_name(company[0])
        company_code_name = REGEX_RG.findall(company[1])[0].replace("\n", "")
        new_root_path = f'{root}[{company_name}]_[{company_code_name}]'
        check_and_make_folder(new_root_path)
        self.move_to(new_root_path)
        Blue(logging.info,
             f"==========End Move Finish Folder in {self.path}==========")
