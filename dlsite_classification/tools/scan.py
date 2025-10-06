import os


def get_folder_cla_struct(path: str) -> dict[str, dict[str, str]]:
    folder_structure: dict[str, dict[str, str]] = {}

    for company in os.listdir(path):
        company_entries = folder_structure.setdefault(company, {})
        for work in os.listdir(os.path.join(path, company)):
            company_entries[work] = os.path.join(path, company, work)

    return folder_structure
