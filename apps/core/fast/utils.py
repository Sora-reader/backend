import orjson
from django.http.response import HttpResponse


def get_fast_response(data: dict) -> HttpResponse:
    return HttpResponse(
        orjson.dumps(data),
        content_type="application/json",
    )
