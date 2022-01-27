
import os
import logging

from dlsite_classification.spkg.logs import Red, Green
from dlsite_classification.tools.scan import get_folder_cla_struct


class FolderCompare:

    def __init__(self, origin_path: str, compare_path: str):
        self.origin_path = origin_path
        self.compare_path = compare_path

    def compare(self):
        origin_folder_data = get_folder_cla_struct(self.origin_path)

        for i in os.listdir(self.compare_path):
            if origin_folder_data.get(i, None) == None:
                continue
            for j in os.listdir(os.path.join(self.compare_path, i)):
                if origin_folder_data.get(i, dict()).get(j, None) == None:
                    continue
                Red(logging.error,
                    f"[Duplicate] Company : 『{i}』 - work :『{j}』.", False)
        Green(logging.info, "Scan finish.")
