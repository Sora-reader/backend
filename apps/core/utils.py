import re


def url_prefix(url: str) -> str:
    return re.match(r"(^https?://(.*))/.*$", url).group(1)
