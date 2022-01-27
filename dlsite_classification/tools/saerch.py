import os
import logging

from dlsite_classification.common.regex import REGEX_RJ
from dlsite_classification.spkg.logs import Green, Yellow


def search_file_code(path):
    logging.info(f"Search Path: {path}")

    def for_check(data: list) -> str:
        for name in data:
            result = REGEX_RJ.findall(name)
            if len(result) != 0:
                Green(logging.info, f"Search - Success {path}")
                return result[0]
        Yellow(logging.info, f"Search - Fail {path}")
        return ''

    for _, folder_Names, file_Names in os.walk(path):
        result = for_check(folder_Names)
        if len(result) != 0:
            return result
        result = for_check(file_Names)
        if len(result) != 0:
            return result
