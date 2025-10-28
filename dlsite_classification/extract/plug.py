from collections.abc import Iterator

from .structure import Company


def extract_folder_path(table: dict[str, Company]) -> Iterator[str]:
    for company_item in table.values():
        for work_item in company_item.work_item.values():
            yield work_item.path
