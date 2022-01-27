import re

REGEX_COMPANY_FOLDER = re.compile(r"^\[[^\]]+]$")
REGEX_RJ = re.compile(r"[BRV][EJ]\d{6}")
REGEX_PATH_REPLACE = re.compile(r'[\\/:*?\"<>|]')
