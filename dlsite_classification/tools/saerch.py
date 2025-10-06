import logging
import os
from typing import cast

from dlsite_classification.common.regex import REGEX_RJ
from dlsite_classification.spkg.logs import Green, Yellow


def search_file_code(path: str) -> str:
    logging.info(f"Search Path: {path}")

    def for_check(data: list[str]) -> str:
        for name in data:
            result = cast(list[str], REGEX_RJ.findall(name))
            if len(result) != 0:
                Green(logging.info, f"Search - Success {path}")
                return result[0]
        Yellow(logging.info, f"Search - Fail {path}")
        return ""

    for _, folder_names, file_names in os.walk(path):
        result = for_check(folder_names)
        if len(result) != 0:
            return result
        result = for_check(file_names)
        if len(result) != 0:
            return result
    return ""
