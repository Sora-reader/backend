import re
from typing import Type

import redis
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db.models import Model, Case, When, IntegerField
from django.shortcuts import _get_queryset  # noqa


def init_redis_client() -> redis.Redis:
    return redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)


def url_prefix(url: str) -> str:
    return re.match(r"(^https?://(.*))/.*$", url).group(1)


@sync_to_async
def async_es_search_to_queryset(search: dict, keep_order=True, *, model: Type[Model]):
    results = search['hits']['hits']
    pks = [res['_id'] for res in results]
    qs = model.objects.filter(pk__in=pks)

    if keep_order:
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(pks)],
            output_field=IntegerField()
        )
        qs = qs.order_by(preserved_order)

    return list(qs)
