from typing import Dict

from django.core.cache import cache
from scrapy import Spider

from apps.manga.annotate import manga_to_annotated_dict
from apps.manga.api.schemas import ChapterListOut, ImageListOut, MangaOut
from apps.parse.types import ParsingStatus
from apps.readmanga.chapter import ReadmangaChapterSpider
from apps.readmanga.detail import ReadmangaDetailSpider
from apps.readmanga.images import ReadmangaImageSpider

CACHE_SAVE_LOGIC: Dict[any, dict] = {
    ReadmangaDetailSpider: {
        "key_getter": lambda manga: manga.source_url,
        "convert": lambda manga: MangaOut(
            status=ParsingStatus.up_to_date.value,
            data=manga_to_annotated_dict(manga),
        ),
        "timeout": 3600 * 24 * 7,
    },
    ReadmangaChapterSpider: {
        "key_getter": lambda chapter_data: chapter_data["rss_url"],
        "convert": lambda chapter_data: ChapterListOut(
            status=ParsingStatus.up_to_date.value,
            data=chapter_data["chapters"],
        ),
        "timeout": 3600,
    },
    ReadmangaImageSpider: {
        "key_getter": lambda images_data: images_data["chapter_url"],
        "convert": lambda images_data: ImageListOut(
            status=ParsingStatus.up_to_date, data=images_data["images"]
        ),
        "timeout": 3600 * 8,
    },
}


class BasePipeline:
    @staticmethod
    def save_to_cache(data, spider: Spider):
        """Save item to cache."""
        save_logic = CACHE_SAVE_LOGIC.get(spider.__class__)
        if not save_logic:
            return

        spider.logger.info("Saving data to cache")
        key_getter = save_logic["key_getter"]
        timeout = save_logic["timeout"]
        convert = save_logic.get("convert")

        key = key_getter(data)
        if convert:
            data = convert(data)
        cache.set(key, data, timeout=timeout)
