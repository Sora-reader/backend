import re
from typing import Union


def is_valid_description(description: Union[list, str]) -> bool:
    if isinstance(description, list):
        if len(description) == 1:
            description = description[0]
        else:
            return False

    word_count = 0
    if description:
        word_count = len(description.split(' '))
    else:
        return False

    if word_count > 1:
        return True
    else:
        return False


def clear_string(s: str) -> Union[str, None]:
    s = re.sub(r'[\n(\xa0)\r]+', '', s)
    if re.fullmatch(r'\s+', s):
        return ''
    return s


def clear_list_description(descs: list) -> str:
    cleaned = [clear_string(s) for s in descs]

    if cleaned is None:
        return ''

    cleaned = list(filter(any, cleaned))
    if len(cleaned) > 0:
        return cleaned[0]
    else:
        return ''
