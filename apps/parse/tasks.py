import logging

import django_rq
import requests
from django.conf import settings
from django.core.cache import caches
from django_rq import job
from scrapy.utils.project import get_project_settings
from scrapyscript import Job, Processor

from apps.manga.models import Chapter, Manga, SaveListMangaThrough
from apps.mangachan import Mangachan
from apps.parse.catalogue import Catalogue
from apps.parse.exceptions import ParsingError, to_error_schema
from apps.parse.types import CacheType, ParserType, ParsingStatus
from apps.readmanga import Readmanga

logger = logging.getLogger("scrapyscript")


@job
def run_spider_task(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    catalogue = Catalogue.from_name(catalogue_name)
    spider = catalogue.from_parser_name(parser_type)
    cache = None

    j = Job(spider, url=url)
    p = Processor(settings=get_project_settings())

    if url:
        cache = caches[CacheType.from_parser_type(parser_type)]
        cache.set(url, ParsingStatus.parsing)

    p.run(j)

    if p.errors:
        errors = [f"{str(cls)}={val}" for cls, val in p.errors]
        msg = "Parsing failed with errors:\n" + "\n".join(errors)
        if url:
            cache.set(url, to_error_schema(msg))
        raise ParsingError(msg)

    if url:
        cache_res = cache.get(url)
        if cache_res == ParsingStatus.parsing.value:
            msg = "Parsing failed but returned no errors, please, try again later."
            cache.set(url, to_error_schema(msg))
            raise ParsingError(msg)


def parse_manga_deep(manga_id: int, parse_images=True):
    # TODO: Add cache checks
    manga = Manga.objects.get(id=manga_id)

    # Details
    logger.info(f"Running detail parser for {manga}")
    run_spider_task(ParserType.detail, "readmanga", url=manga.source_url)
    manga.refresh_from_db()

    # Chapters
    logger.info("Running chapter parser")
    run_spider_task(ParserType.chapter, "readmanga", url=manga.chapters_url)

    if not parse_images:
        logger.info("Skipping further steps as parse_images is set to False")
        return

    # Get images from middle chapter
    chapters = manga.chapters.all()
    chapters_len = len(chapters)

    if not chapters:
        logger.warning(f"No chapters found for {manga}")
        return

    middle_chapter: Chapter = chapters[chapters_len // 2]
    logger.info(f"Running image parser for {middle_chapter}")
    run_spider_task(ParserType.image, "readmanga", url=middle_chapter.link)

    # Get middle image size
    images = caches[CacheType.image].get(middle_chapter.link)
    images_len = len(images)

    if not images:
        logger.warning(f"No images found chapter {middle_chapter}")
        return

    middle_image = images[images_len // 2]
    image_response = requests.get(middle_image)

    chapter_size_kb = len(image_response.content) / 1024 * images_len
    manga_size_kb = chapter_size_kb * chapters_len

    if not manga_size_kb > settings.MANGA_MAX_SIZE_KB:
        logger.info(f"Manga size is ok (~{manga_size_kb // 1024}MB)")

        # Remove middle chapter from parsing
        del chapters[chapters_len // 2]
        chapters_len -= 1

        for num, chapter in enumerate(chapters, 1):
            logger.info(f"Running image parser for chapter {num}/{chapters_len}")
            run_spider_task(ParserType.image, "readmanga", url=chapter.link)


@job
def update_lists_details():
    manga_ids = SaveListMangaThrough.objects.values_list("manga_id", flat=True).distinct()
    ids_len = len(manga_ids)
    for num, manga_id in enumerate(manga_ids, 1):
        logger.info(f"Updating deep #{manga_id} ({num}/{ids_len})")
        parse_manga_deep(manga_id, parse_images=False)


scheduler = django_rq.get_scheduler("default")
scheduler.cron(
    "0 0 * * *",
    func=run_spider_task,
    args=[ParserType.list, Readmanga.name],
    queue_name="default",
    use_local_timezone=False,
)
scheduler.cron(
    "0 1 * * *",
    func=run_spider_task,
    args=[ParserType.list, Mangachan.name],
    queue_name="default",
    use_local_timezone=False,
)
scheduler.cron(
    "0 2 * * *", func=update_lists_details, queue_name="default", use_local_timezone=False
)
