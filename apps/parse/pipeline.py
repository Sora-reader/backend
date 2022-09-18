from typing import Dict

from django.core.cache import cache
from scrapy import Spider

from apps.manga.api.schemas import ChapterOut, ChapterSchema, MangaDetail, MangaSchema
from apps.parse.types import ParsingStatus
from apps.readmanga.chapter import ReadmangaChapterSpider
from apps.readmanga.detail import ReadmangaDetailSpider
from apps.readmanga.images import ReadmangaImageSpider

CACHE_SAVE_LOGIC: Dict[any, dict] = {
    ReadmangaDetailSpider: {
        "key_getter": lambda manga: manga.source_url,
        "convert": lambda manga: MangaDetail(
            status=ParsingStatus.up_to_date.value,
            data=MangaSchema.from_orm(manga),
        ),
        "timeout": 3600 * 24 * 7,
    },
    ReadmangaChapterSpider: {
        "key_getter": lambda chapter: chapter.link,
        "convert": lambda chapter: ChapterOut(
            status=ParsingStatus.up_to_date.value,
            data=ChapterSchema.from_orm(chapter),
        ),
        "timeout": 3600 * 12,
    },
    ReadmangaImageSpider: {
        "key_getter": lambda images_item: images_item["chapter_url"],
        "convert": lambda images_item: images_item["images"],
        "timeout": 3600 * 8,
    },
}


class BasePipeline:
    @staticmethod
    def save_to_cache(data, spider: Spider):
        """Save item to cache."""
        spider.logger.info("Saving data to cache")
        save_logic = CACHE_SAVE_LOGIC[spider.__class__]

        key_getter = save_logic["key_getter"]
        timeout = save_logic["timeout"]
        convert = save_logic.get("convert")

        key = key_getter(data)
        if convert:
            data = convert(data)
        cache.set(key, data, timeout=timeout)
