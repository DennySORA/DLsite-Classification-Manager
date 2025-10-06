import asyncio
import logging
import os
import shutil
import time
from os import path as os_path

from dlsite_classification.common.regex import REGEX_RG, REGEX_RJ
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red, Yellow
from dlsite_classification.tools import (
    check_and_make_folder,
    check_folder_has_file,
    merge_folder_name_move,
    replace_file_name,
    save_data,
)


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
        file_name = replace_file_name(f"{name}.tag")
        file_path = os_path.join(info_folder_path, file_name)
        await save_data(file_path, "\n".join(data))

    async def _save_images(self, path: str, images: list | None = None):
        if images is None:
            images = self.file_info.get("images", None)
        if images is None:
            return
        Blue(logging.info, f"Save {self.folder_name} image.")
        await asyncio.gather(
            *[
                save_data(
                    os_path.join(
                        path,
                        i.get("name", ""),
                    ),
                    i.get("data", ""),
                )
                for i in images
            ]
        )

    async def _merge_old_tags(self, new_info_path: str, old_tags: dict):
        """Merge old tags with new tags, preserving unique values"""
        Blue(logging.info, f"Merging old tags with new tags for {self.folder_name}")
        for tag_file, old_values in old_tags.items():
            new_tag_path = os_path.join(new_info_path, tag_file)
            if os_path.isfile(new_tag_path):
                try:
                    # Read new values
                    with open(new_tag_path, encoding="utf-8") as f:
                        new_values = f.read().strip().split("\n")

                    # Merge: preserve order, add old values that are not in new values
                    merged_values = new_values.copy()
                    for old_val in old_values:
                        if old_val.strip() and old_val not in new_values:
                            merged_values.append(old_val)

                    # Write merged values back
                    with open(new_tag_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(merged_values))
                    Blue(logging.info, f"Merged tag file {tag_file}")
                except Exception as e:
                    Yellow(logging.warning, f"Failed to merge tag {tag_file}: {e}")

    def _get_rename(self, code: str, is_company: bool = False) -> str:
        # Get Title and company
        title = self.file_info.get("title", list())[0]
        company = self.file_info.get("company", list())
        company_name = company[0]
        company_code_name = REGEX_RG.findall(company[1])[0].replace("\n", "")

        if is_company:
            return os_path.join(
                os_path.split(self.root_path)[0],
                replace_file_name(f"[{company_name}]_[{company_code_name}]"),
            )
        return os_path.join(
            self.root_path,
            replace_file_name(
                f"[{code}]_[{company_name}]_[{company_code_name}] {title}"
            ),
        )

    # ---------------------------------------
    # ---------------------------------------
    # ---------------------------------------

    def use_crawler(self, crawler):
        self.crawler = crawler

    def move_to(self, folder_name, new_name=None):
        code_path = os_path.join(self.root_path, folder_name)
        Cyan(logging.info, f"Move Folder {self.root_path} TO {code_path} - {new_name}")

        # check folder is existed.
        check_and_make_folder(code_path)

        # Move file.
        if new_name == None:
            new_name = self.folder_name
        new_path = os_path.join(code_path, new_name)

        if os_path.isdir(new_path):
            duplicate_path = os_path.join(self.root_path, "duplicate")
            check_and_make_folder(duplicate_path)
            new_path = os_path.join(duplicate_path, f"{new_name}_{time.time()}")

        try:
            file = open(
                os_path.join(self.path, ".dlsite_classification.path.old"),
                "a+",
                encoding="utf-8",
            )
            file.write(self.path + "\n")
            file.write(new_path + "\n")
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
        Cyan(
            logging.info,
            f"==========Start Check Folder Recursive in {self.path}==========",
        )

        has_file, data = check_folder_has_file(self.path)
        data_count = len(data)
        if data_count > 1 or has_file:
            Cyan(
                logging.info,
                f"==========End Check Folder Recursive because Has Data in {self.path}==========",
            )
            return
        if data_count == 0:
            self.move_to("null")
            Cyan(
                logging.info,
                f"==========End Check Folder Recursive because Null in {self.path}==========",
            )
            return
        if data_count == 1:
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
                self.move_to("code", code[0])
            self.file_info["code"] = str(code[0])
            return "code"
        if is_move:
            self.move_to("other")
        return "other"

    async def set_request_failed(self):
        if self.crawler is None:
            raise Exception("Not use crawler.")
        code = self.crawler.code
        info_folder_path = os_path.join(self.path, code + "_info")
        await self._save_tag(
            info_folder_path, "request_failed", f"Request Failed :{time.time()}"
        )

    def get_info(self) -> bool:
        if self.crawler is None:
            raise Exception("Not use crawler.")
        self.file_info = self.crawler.get_info()
        if self.file_info is None:
            return False
        return True

    async def classify(self, is_move=True, merge_tags=False):
        Cyan(logging.info, f"==========Start Classify Folder in {self.path}==========")
        # Create info folder
        code = self.file_info.get("code", "")
        info_folder_path = os_path.join(self.path, code + "_info")
        temp_info_folder_path = os_path.join(self.path, code + "_info_temp")

        # User custom tag files to preserve
        user_custom_tags = ["my_rating.tag", "my_collection.tag", "my_collections.tag"]

        # Save old user custom tags if they exist
        old_user_tags = {}
        if os_path.isdir(info_folder_path):
            for tag_file in user_custom_tags:
                old_tag_path = os_path.join(info_folder_path, tag_file)
                if os_path.isfile(old_tag_path):
                    try:
                        with open(old_tag_path, encoding="utf-8") as f:
                            old_user_tags[tag_file] = f.read()
                    except Exception as e:
                        Yellow(
                            logging.warning, f"Failed to read old tag {tag_file}: {e}"
                        )

        # Save old tags for merging if merge_tags is enabled
        old_tags = {}
        if merge_tags and os_path.isdir(info_folder_path):
            Cyan(logging.info, f"Merging tags mode enabled for {code}")
            for tag_file in os.listdir(info_folder_path):
                if tag_file.endswith(".tag") and tag_file not in user_custom_tags:
                    old_tag_path = os_path.join(info_folder_path, tag_file)
                    try:
                        with open(old_tag_path, encoding="utf-8") as f:
                            old_tags[tag_file] = f.read().strip().split("\n")
                    except Exception as e:
                        Yellow(logging.warning, f"Failed to read tag {tag_file}: {e}")

        # Create temporary folder for new data
        if os_path.isdir(temp_info_folder_path):
            shutil.rmtree(temp_info_folder_path)
        check_and_make_folder(temp_info_folder_path)

        try:
            # Save new data to temporary folder
            await asyncio.gather(
                self._save_images(temp_info_folder_path),
                *[
                    self._save_tag(temp_info_folder_path, key, val)
                    for key, val in self.file_info.items()
                    if key != "images"
                ],
            )

            # Merge tags if enabled
            if merge_tags and old_tags:
                await self._merge_old_tags(temp_info_folder_path, old_tags)

            # Restore user custom tags
            for tag_file, content in old_user_tags.items():
                try:
                    tag_path = os_path.join(temp_info_folder_path, tag_file)
                    with open(tag_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    Blue(logging.info, f"Restored user tag {tag_file}")
                except Exception as e:
                    Yellow(logging.warning, f"Failed to restore tag {tag_file}: {e}")

            # Success: remove old folder and rename temp folder
            if os_path.isdir(info_folder_path):
                shutil.rmtree(info_folder_path)
            os.rename(temp_info_folder_path, info_folder_path)
            Green(logging.info, f"Successfully updated info for {code}")

        except Exception as e:
            # Failure: remove temp folder and keep old data
            if os_path.isdir(temp_info_folder_path):
                shutil.rmtree(temp_info_folder_path)
            Red(logging.error, f"Failed to update info for {code}: {e}")
            raise

        if is_move:
            # Move folder
            self.move_to(self.path, self._get_rename(code))

        Blue(logging.info, f"==========End Classify Folder in {self.path}==========")

    async def rename(self, is_company: bool = False):
        code = self.file_info.get("code", "")

        if is_company:
            path = self._get_rename(code, True)
            if not os_path.exists(path):
                os.rename(self.root_path, path)
        else:
            os.rename(self.path, self._get_rename(code))

    def finish(self):
        Cyan(
            logging.info, f"==========Start Move Finish Folder in {self.path}=========="
        )
        root = os_path.join(self.root_path, "../../finish/")
        company = self.file_info.get("company", list())
        if len(company) == 0:
            Yellow(logging.warning, "Not company in {self.path}")
            return
        company_name = replace_file_name(company[0])
        company_code_name = REGEX_RG.findall(company[1])[0].replace("\n", "")
        new_root_path = f"{root}[{company_name}]_[{company_code_name}]"
        check_and_make_folder(new_root_path)
        self.move_to(new_root_path)
        Blue(logging.info, f"==========End Move Finish Folder in {self.path}==========")
