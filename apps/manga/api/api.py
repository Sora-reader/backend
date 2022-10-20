from typing import List, Tuple

from django.core.cache import cache
from django.http import Http404
from ninja import Router

from apps.manga.annotate import manga_to_annotated_dict
from apps.manga.api.schemas import (
    ChapterListOut,
    ErrorSchema,
    ImageListOut,
    MangaOut,
    MangaSchema,
    MessageSchema,
    ParsingSchemaOut,
)
from apps.manga.models import Chapter, Manga
from apps.parse.parser import CHAPTER_PARSER, DETAIL_PARSER, IMAGE_PARSER
from apps.parse.tasks import run_spider_task
from apps.parse.types import ParsingStatus
from apps.typesense_bind.query import query_dict_list_by_title

router = Router(tags=["Manga"])


def with_error_schema(schema):
    return {200: schema, 400: ErrorSchema, 425: MessageSchema}


def is_error_payload(data):
    return hasattr(data, "error")


def handle_parsing_with_caching(
    spider: str,
    link: str,
    fallback: ParsingSchemaOut,
) -> Tuple[int, ParsingSchemaOut | ErrorSchema]:
    """
    Abstract logic of handling cache statuses and results/errors.

    :param spider: Spider name.
    :param link: Parsing link and a cache key.
    :param fallback: Fallback response value for when parsing just started or already running.

    Scenarios:
        1. "parsing" value inside cache means parsing is already running -> return fallback value.
        2. An error inside cache means previous run failed -> return error and clear cache.
            (next request wil rerun parsing)
        3. Empty cache means we need to run parsing -> run spider and return fallback value.
        4. Nothing from above means there can only be parsed data inside cache -> return it.
    """
    parsing_cache = cache.get(link)

    if parsing_cache and parsing_cache != ParsingStatus.parsing.value:
        # If there's an error in cache, then it means parsing failed
        # Return the error and clear cache to rerun parsing on next request
        if is_error_payload(parsing_cache):
            cache.delete(link)
            return 400, parsing_cache

        # Return parsing payload if everything's ok
        return parsing_cache

    # Run tasks only if there's no results or parsing status inside cache
    elif not parsing_cache:
        # Put task into queue
        run_spider_task.delay(spider, url=link)

    return 200, fallback


def get_manga_or_404(pk, prefetch: List[str] = None):
    manga = Manga.objects.filter(pk=pk).prefetch_related(*(prefetch or [])).first()
    if not manga:
        raise Http404("No manga found")
    return manga


@router.get("/search/", response=List[MangaSchema])
def search_manga(request, title: str):
    return query_dict_list_by_title(title)


@router.get("/{manga_id}/", response=with_error_schema(MangaOut))
def get_manga(request, manga_id: int):
    manga = get_manga_or_404(pk=manga_id)

    return handle_parsing_with_caching(
        DETAIL_PARSER,
        manga.source_url,
        MangaOut(status=ParsingStatus.parsing.value, data=manga_to_annotated_dict(manga)),
    )


@router.get("/{manga_id}/chapters/", response=with_error_schema(ChapterListOut))
def get_chapters(request, manga_id: int):
    manga = get_manga_or_404(pk=manga_id, prefetch=["chapters"])

    if not manga.rss_url:
        print(manga, manga.rss_url)
        return 425, MessageSchema(message="Detail's were not yet parsed")

    return handle_parsing_with_caching(
        CHAPTER_PARSER,
        manga.rss_url,
        ChapterListOut(status=ParsingStatus.parsing.value, data=list(manga.chapters.all())),
    )


@router.get("/{manga_id}/chapters/{chapter_id}/images/", response=with_error_schema(ImageListOut))
def get_chapter_images(request, manga_id: int, chapter_id: int):
    chapter = Chapter.objects.filter(pk=chapter_id, manga_id=manga_id).first()

    if not chapter:
        return 400, ErrorSchema(error="No chapter found")

    res = handle_parsing_with_caching(
        IMAGE_PARSER,
        chapter.link,
        ImageListOut(status=ParsingStatus.parsing.value, data=[]),
    )

    return res
