from typing import Union

import redis
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def format_error_response(
    error: Union[Exception, str],
    status_code=HTTP_400_BAD_REQUEST,
) -> Response:
    """Format error to DRF's Response"""

    return Response({"error": str(error)}, status=status_code)


def init_redis_client() -> redis.Redis:
    return redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)
