import redis
from django.conf import settings


def init_redis_client() -> redis.Redis:
    return redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)
