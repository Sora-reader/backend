from functools import reduce
from typing import List

from django.shortcuts import get_object_or_404
from elasticsearch_dsl import Q
from ninja import Router

from apps.manga.api.schemas import MangaOut
from apps.manga.documents import MangaDocument
from apps.manga.models import Manga

router = Router(tags=["Manga"])


@router.get("/search", response=List[MangaOut])
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


@router.get("/{manga_id}", response=MangaOut)
def get_manga(request, manga_id: int):
    manga = get_object_or_404(Manga, id=manga_id)
    return manga
