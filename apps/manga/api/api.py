from functools import reduce
from typing import List

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from elasticsearch_dsl import Q
from ninja import Router

from apps.manga.api.schemas import MangaDetail, MangaSchema
from apps.manga.documents import MangaDocument
from apps.manga.models import Manga
from apps.parse.tasks import run_spider_task
from apps.parse.types import ParsingStatus

router = Router(tags=["Manga"])


@router.get("/search", response=List[MangaSchema])
def search_manga(request, title: str):
    title = title.split(" ")

    def fuzzy_query(title_part: str):
        return Q("fuzzy", title=title_part)

    if len(title) > 1:
        query = reduce(lambda a, b: fuzzy_query(a) | fuzzy_query(b), title)
    else:
        query = fuzzy_query(title[0])

    qs = MangaDocument.search().query(query).to_queryset()
    return qs


@router.get("/{manga_id}", response=MangaDetail)
def get_manga(request, manga_id: int):
    manga = get_object_or_404(Manga, id=manga_id)

    cache_entry = cache.get(manga.source_url)
    if cache_entry and cache_entry != ParsingStatus.parsing.value:
        return cache_entry
    else:
        run_spider_task.delay("detail", url=manga.source_url)

    return MangaDetail(
        status=ParsingStatus.parsing.value,
        data=manga,
    )
