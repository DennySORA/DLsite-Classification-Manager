
import os


def get_folder_cla_struct(path: str) -> dict[str, dict[str, str]]:
    folder_structure = dict()

    for i in os.listdir(path):
        if folder_structure.get(i, None) == None:
            folder_structure[i] = dict()
        for j in os.listdir(os.path.join(path, i)):
            folder_structure[i][j] = os.path.join(path, i, j)

    return folder_structure
