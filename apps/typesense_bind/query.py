from django.db.models import Case, IntegerField, When
from typesense.documents import Documents

from apps.manga.models import Manga
from apps.typesense_bind.client import get_ts_client
from apps.typesense_bind.schema import schema_name


def get_query_base() -> Documents:
    return get_ts_client().collections[schema_name].documents


def query_by_title(title: str):
    search_parameters = {
        "include_fields": ["id"],
        "q": title,
        "query_by": "title",
    }

    res = get_query_base().search(search_parameters)["hits"]
    pks = [r["document"]["id"] for r in res]

    preserved_order = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(pks)], output_field=IntegerField()
    )
    return Manga.objects.filter(pk__in=pks).order_by(preserved_order)
