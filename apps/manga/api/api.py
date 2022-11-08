from typing import List, Optional, Tuple

from django.conf import settings
from django.core.cache import caches
from ninja import Router

from apps.core.api.schemas import ErrorSchema, MessageSchema
from apps.core.api.utils import get_model_or_404, sora_schema
from apps.manga.annotate import manga_to_annotated_dict
from apps.manga.api.schemas import (
    ChapterListOut,
    ImageListOut,
    MangaOut,
    MangaSchema,
    ParsingSchemaOut,
)
from apps.manga.models import Chapter, Manga
from apps.mangachan import Mangachan
from apps.parse.exceptions import ParsingError
from apps.parse.tasks import run_spider_task
from apps.parse.types import CacheType, ParserType, ParsingStatus
from apps.typesense_bind.query import query_dict_list_by_title

manga_router = Router(tags=["Manga"])


def is_error_payload(data):
    return hasattr(data, "error")


def handle_parsing_with_caching(
    parser_type: str,
    catalogue: str,
    link: str,
    fallback: ParsingSchemaOut,
    cache_type: Optional[str] = None,
) -> Tuple[int, ParsingSchemaOut | ErrorSchema]:
    """
    Abstract logic of handling cache statuses and results/errors.

    :param parser_type: Parser type.
    :param catalogue: Catalogue name.
    :param link: Parsing link and a cache key.
    :param fallback: Fallback response value for when parsing just started or already running.
    :param cache_type: Cache which will be used to extract data. Can be used when running,
    for example, detail spider which also writes to chapter cache

    Scenarios:
        1. "parsing" value inside cache means parsing is already running -> return fallback value.
        2. An error inside cache means previous run failed -> return error and clear cache.
            (next request wil rerun parsing)
        3. Empty cache means we need to run parsing -> run spider and return fallback value.
        4. Nothing from above means there can only be parsed data inside cache -> return it.
    """
    if not cache_type:
        cache_type = CacheType.from_parser_type(parser_type)
    cache = caches[cache_type]
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
        f = run_spider_task
        if not settings.DEBUG:
            f = f.delay
        try:
            f(parser_type, catalogue_name=catalogue, url=link)
        except ParsingError as e:
            return 400, ErrorSchema(error=str(e))

    return 200, fallback


@manga_router.get("/search/", response=List[MangaSchema])
def search_manga(request, title: str):
    return query_dict_list_by_title(title)


@manga_router.get("/{manga_id}/", response=sora_schema(MangaOut))
def get_manga(request, manga_id: int):
    manga = get_model_or_404(Manga, pk=manga_id)

    return handle_parsing_with_caching(
        ParserType.detail,
        manga.source,
        manga.source_url,
        MangaOut(status=ParsingStatus.parsing.value, data=manga_to_annotated_dict(manga)),
    )


@manga_router.get("/{manga_id}/chapters/", response=sora_schema(ChapterListOut))
def get_chapters(request, manga_id: int):
    manga = get_model_or_404(Manga, pk=manga_id, prefetch=["chapters"])

    if not manga.chapters_url:
        return 425, MessageSchema(message="Details were not yet parsed.")

    return handle_parsing_with_caching(
        ParserType.detail if manga.source == Mangachan.name else ParserType.chapter,
        manga.source,
        manga.chapters_url,
        ChapterListOut(status=ParsingStatus.parsing.value, data=list(manga.chapters.all())),
        CacheType.chapter,
    )


@manga_router.get("/{manga_id}/chapters/{chapter_id}/images/", response=sora_schema(ImageListOut))
def get_chapter_images(request, manga_id: int, chapter_id: int):
    chapter = (
        Chapter.objects.filter(pk=chapter_id, manga_id=manga_id).prefetch_related("manga").first()
    )

    if not chapter:
        return 400, ErrorSchema(error="No chapter found.")

    res = handle_parsing_with_caching(
        ParserType.image,
        chapter.manga.source,
        chapter.link,
        ImageListOut(status=ParsingStatus.parsing.value, data=[]),
    )

    return res
