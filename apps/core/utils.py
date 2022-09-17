import re

import redis
from django.conf import settings


def init_redis_client() -> redis.Redis:
    return redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)


def url_prefix(url: str) -> str:
    return re.match(r"(^https?://(.*))/.*$", url).group(1)
