"""Helper module for saving work information to disk.

This module provides reusable functions to fetch work information from DLsite
and save it to a specified directory. Used by both regular classification workflow
and the ARCHIVE feature.
"""

import asyncio
import logging
import os
import shutil
from collections.abc import Iterable
from os import path as os_path
from typing import Any

from dlsite_classification.crawler.work import DLsiteWorkCrawler
from dlsite_classification.spkg.logs import Blue, Green, Red, Yellow
from dlsite_classification.tools import (
    check_and_make_folder,
    replace_file_name,
    save_data,
)


async def _save_tag(
    info_folder_path: str,
    name: str,
    data: Iterable[str] | str | None = None,
) -> None:
    """Save a single tag file.

    Args:
        info_folder_path: Path to the info folder
        name: Tag name (will be saved as {name}.tag)
        data: Tag data (string, iterable, or None)
    """
    if data is None:
        return
    if isinstance(data, str):
        values = [data]
    elif isinstance(data, bytes):
        values = [data.decode("utf-8", errors="ignore")]
    elif isinstance(data, Iterable):
        values = [str(item) for item in data if str(item)]
    else:
        values = [str(data)]
    if not values:
        return

    check_and_make_folder(info_folder_path)

    file_name = replace_file_name(f"{name}.tag")
    file_path = os_path.join(info_folder_path, file_name)
    await save_data(file_path, "\n".join(values))


async def _save_images(path: str, images: list[dict[str, Any]] | None = None) -> None:
    """Save work images to disk.

    Args:
        path: Path to save images
        images: List of image dicts with 'name' and 'data' keys
    """
    if images is None:
        return

    await asyncio.gather(
        *[
            save_data(
                os_path.join(path, img.get("name", "")),
                img.get("data", ""),
            )
            for img in images
        ]
    )


async def save_work_info_to_path(
    work_code: str,
    target_path: str,
    preserve_user_tags: bool = True,
    merge_existing_tags: bool = False,
) -> bool:
    """Fetch work info from DLsite and save to specified path.

    This function creates a {work_code}_info folder at the target path,
    fetches work information from DLsite, and saves all metadata and images.

    Args:
        work_code: DLsite work code (e.g., 'RJ123456')
        target_path: Base path where {work_code}_info will be created
        preserve_user_tags: Whether to preserve existing user custom tags
        merge_existing_tags: Whether to merge with existing tags

    Returns:
        True if successful, False otherwise

    Example:
        >>> await save_work_info_to_path(
        ...     "RJ123456", "/data/company/ARCHIVE", preserve_user_tags=False
        ... )
        # Creates /data/company/ARCHIVE/RJ123456_info/ with all metadata
    """
    try:
        Blue(logging.info, f"Saving work info for {work_code} to {target_path}")

        # Create info folder path
        info_folder_path = os_path.join(target_path, f"{work_code}_info")
        temp_info_folder_path = os_path.join(target_path, f"{work_code}_info_temp")

        # User custom tags to preserve
        user_custom_tags = ["my_rating.tag", "my_collection.tag", "my_collections.tag"]

        # Save existing user tags if requested
        old_user_tags = {}
        if preserve_user_tags and os_path.isdir(info_folder_path):
            for tag_file in user_custom_tags:
                old_tag_path = os_path.join(info_folder_path, tag_file)
                if os_path.isfile(old_tag_path):
                    try:
                        with open(old_tag_path, encoding="utf-8") as f:
                            old_user_tags[tag_file] = f.read()
                    except Exception as e:
                        Yellow(logging.warning, f"Failed to read {tag_file}: {e}")

        # Save existing tags for merging if requested
        old_tags = {}
        if merge_existing_tags and os_path.isdir(info_folder_path):
            for tag_file in os.listdir(info_folder_path):
                if tag_file.endswith(".tag") and tag_file not in user_custom_tags:
                    old_tag_path = os_path.join(info_folder_path, tag_file)
                    try:
                        with open(old_tag_path, encoding="utf-8") as f:
                            old_tags[tag_file] = f.read().strip().split("\n")
                    except Exception as e:
                        Yellow(logging.warning, f"Failed to read {tag_file}: {e}")

        # Fetch work info from DLsite
        crawler = DLsiteWorkCrawler(code=work_code)
        await crawler.get_use_code()
        work_info = crawler.get_info()

        if not work_info:
            Red(logging.error, f"Failed to fetch info for {work_code}")
            return False

        # Create temporary folder
        if os_path.isdir(temp_info_folder_path):
            shutil.rmtree(temp_info_folder_path)
        check_and_make_folder(temp_info_folder_path)

        try:
            # Save all data to temporary folder
            await asyncio.gather(
                _save_images(temp_info_folder_path, work_info.get("images")),
                *[
                    _save_tag(temp_info_folder_path, key, val)
                    for key, val in work_info.items()
                    if key != "images"
                ],
            )

            # Merge old tags if requested
            if merge_existing_tags and old_tags:
                await _merge_tags(temp_info_folder_path, old_tags)

            # Restore user custom tags
            for tag_file, content in old_user_tags.items():
                try:
                    tag_path = os_path.join(temp_info_folder_path, tag_file)
                    with open(tag_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception as e:
                    Yellow(logging.warning, f"Failed to restore {tag_file}: {e}")

            # Atomic replace: remove old, rename temp
            if os_path.isdir(info_folder_path):
                shutil.rmtree(info_folder_path)
            os.rename(temp_info_folder_path, info_folder_path)

            Green(logging.info, f"Successfully saved info for {work_code}")
            return True

        except Exception as e:
            # Cleanup temp folder on failure
            if os_path.isdir(temp_info_folder_path):
                shutil.rmtree(temp_info_folder_path)
            Red(logging.error, f"Failed to save info for {work_code}: {e}")
            raise

    except Exception as e:
        Red(logging.error, f"Error processing {work_code}: {e}")
        return False


async def _merge_tags(new_info_path: str, old_tags: dict[str, list[str]]) -> None:
    """Merge old tags with new tags.

    Args:
        new_info_path: Path to new info folder with new tags
        old_tags: Dict of old tag files and their values
    """
    for tag_file, old_values in old_tags.items():
        new_tag_path = os_path.join(new_info_path, tag_file)
        if os_path.isfile(new_tag_path):
            try:
                with open(new_tag_path, encoding="utf-8") as f:
                    new_values = f.read().strip().split("\n")

                # Merge: keep new values, add old values not in new
                merged_values = new_values.copy()
                for old_val in old_values:
                    if old_val.strip() and old_val not in new_values:
                        merged_values.append(old_val)

                with open(new_tag_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(merged_values))
            except Exception as e:
                Yellow(logging.warning, f"Failed to merge {tag_file}: {e}")
