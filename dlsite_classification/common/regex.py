import re

REGEX_COMPANY_FOLDER = re.compile(r"^\[[^\]]+](_\[[^\]]+])?$")
REGEX_RJ = re.compile(r"[BRV][EJ]\d{6,8}")
REGEX_RG = re.compile(r"[BRV]G\d{5}")
REGEX_PATH_REPLACE = re.compile(r'[\\/:*?\"<>|]')
