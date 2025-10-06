from dlsite_classification.common.regex import REGEX_PATH_REPLACE


def replace_file_name(name: str) -> str:
    """Normalize file names by replacing characters invalid on most filesystems."""
    value = str(name)
    return REGEX_PATH_REPLACE.sub("_", value)
