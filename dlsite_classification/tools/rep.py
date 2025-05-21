from dlsite_classification.common.regex import REGEX_PATH_REPLACE


def replace_file_name(name) -> str:
    try:
        name = REGEX_PATH_REPLACE.sub("_", name)
    except:
        pass
    return name
