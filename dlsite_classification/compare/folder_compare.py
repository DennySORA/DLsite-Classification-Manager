import logging
import os

from dlsite_classification.spkg.logs import Green, Red
from dlsite_classification.tools.scan import get_folder_cla_struct


class FolderCompare:
    def __init__(self, origin_path: str, compare_path: str):
        self.origin_path = origin_path
        self.compare_path = compare_path

    def compare(self) -> None:
        origin_folder_data = get_folder_cla_struct(self.origin_path)

        for company in os.listdir(self.compare_path):
            origin_company = origin_folder_data.get(company)
            if origin_company is None:
                continue
            for work in os.listdir(os.path.join(self.compare_path, company)):
                if origin_company.get(work) is None:
                    continue
                Red(
                    logging.error,
                    f"[Duplicate] Company : 『{company}』 - work :『{work}』.",
                    stack_info=False,
                )
        Green(logging.info, "Scan finish.")
