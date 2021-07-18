import redis
from django.core.checks import Warning

from apps.core.utils import init_redis_client


def check_redis(*args, **kwargs):
    errors = []
    client = init_redis_client()
    try:
        client.ping()
    except redis.exceptions.ConnectionError as r_con_error:
        errors.append(
            Warning(
                "Redis unavailable",
                hint="Check REDIS_URL or if redis is running",
                obj=r_con_error,
                id="core.E001",
            )
        )
    return errors
