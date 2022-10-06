import re


def url_prefix(url: str) -> str:
    """
    Return host url prefix.

    For example, when scraped url starts without specifying host '/somePath'
    then, given some other url (like source_url) we can prepend it.

    >>> url_prefix('https://readmanga.live/podniatie_urovnia_v_odinochku__A35c96')
    'https://readmanga.live'
    """
    return re.match(r"(^https?://(.*))/.*$", url).group(1)
