from typing import List

from django.core.cache import cache
from django.http import Http404, HttpResponse
from ninja import Router

from apps.manga.annotate import manga_to_annotated_dict
from apps.manga.api.schemas import ChapterListOut, ImageListOut, MangaOut, MangaSchema
from apps.manga.models import Chapter, Manga
from apps.parse.parser import CHAPTER_PARSER, DETAIL_PARSER, IMAGE_PARSER
from apps.parse.tasks import run_spider_task
from apps.parse.types import ParsingStatus
from apps.typesense_bind.query import query_dict_list_by_title

router = Router(tags=["Manga"])


def get_manga_or_404(pk, prefetch: List[str] = None):
    manga = Manga.objects.filter(pk=pk).prefetch_related(*(prefetch or [])).first()
    if not manga:
        raise Http404("No manga found")
    return manga


@router.get("/search/", response=List[MangaSchema])
def search_manga(request, title: str):
    return query_dict_list_by_title(title)


@router.get("/{manga_id}/", response=MangaOut)
def get_manga(request, manga_id: int):
    manga = get_manga_or_404(pk=manga_id)

    cache_entry = cache.get(manga.source_url)
    if cache_entry and cache_entry != ParsingStatus.parsing.value:
        return cache_entry
    elif not cache_entry:
        cache.set(manga.source_url, ParsingStatus.parsing.value)
        run_spider_task.delay(DETAIL_PARSER, url=manga.source_url)

    return MangaOut(
        status=ParsingStatus.parsing.value,
        data=manga_to_annotated_dict(manga),
    )


@router.get("/{manga_id}/chapters/", response=ChapterListOut)
def get_chapters(request, manga_id: int):
    manga = get_manga_or_404(pk=manga_id, prefetch=["chapters"])

    if not manga.rss_url:
        return HttpResponse(content="Detail's were not yet parsed", status=425)

    cache_entry = cache.get(manga.rss_url)
    if cache_entry and cache_entry != ParsingStatus.parsing.value:
        return cache_entry
    elif not cache_entry:
        cache.set(manga.rss_url, ParsingStatus.parsing.value)
        run_spider_task.delay(CHAPTER_PARSER, url=manga.rss_url)

    return ChapterListOut(
        status=ParsingStatus.parsing.value,
        data=list(manga.chapters.all()),
    )


@router.get("/{manga_id}/chapters/{chapter_id}/images/", response=ImageListOut)
def get_chapter_images(request, manga_id: int, chapter_id: int):
    chapter = Chapter.objects.filter(pk=chapter_id, manga_id=manga_id).first()

    if not chapter:
        raise Http404("No chapter found")

    if cache_entry := cache.get(chapter.link):
        return cache_entry
    else:
        run_spider_task(IMAGE_PARSER, url=chapter.link)

    # Re-request cache data after spider ran
    return ImageListOut(__root__=cache.get(chapter.link))
