
from .structure import Company


def extract_folder_path(table: dict[str, Company]):
    for company_item in table.values():
        for i in company_item.work_item.values():
            yield i.path
