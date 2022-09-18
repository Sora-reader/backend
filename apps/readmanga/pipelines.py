import logging
from copy import deepcopy
from typing import Dict, List, Tuple, Type

from django.db import transaction
from scrapy.spiders import Spider

from apps.core.abc.models import BaseModel
from apps.core.utils import url_prefix
from apps.manga.models import Category, Chapter, Genre, Manga, PersonRelatedToManga, PersonRole
from apps.parse.items import MangaChapterItem
from apps.readmanga.chapter import ReadmangaChapterSpider
from apps.readmanga.images import ReadmangaImageSpider
from apps.readmanga.list import ReadmangaListSpider

logger = logging.getLogger("scrapy")


@transaction.atomic
def bulk_get_or_create(cls: Type[BaseModel], names: List[str]) -> Tuple:
    objects = []
    for name in names:
        objects.append(cls.objects.get_or_create(name=name))
    return tuple(obj for obj, _ in objects)


class ReadmangaImagePipeline:
    @staticmethod
    def process_item(item: Dict[str, List[str]], spider: ReadmangaImageSpider):
        url, images = next(iter(item.items()))
        spider.redis_client.delete(url)
        spider.redis_client.expire(url, Manga.IMAGE_UPDATE_FREQUENCY)
        spider.redis_client.rpush(url, *images)


class ReadmangaChapterPipeline:
    @staticmethod
    def process_item(chapter: MangaChapterItem, _: ReadmangaChapterSpider):
        rss_url = chapter.pop("manga_rss_url")
        manga = Manga.objects.get(rss_url=rss_url)
        Chapter.objects.get_or_create(
            manga=manga,
            **chapter,
        )


class ReadmangaPipeline:
    @staticmethod
    def get_or_create_or_update_manga(spider: Spider, source_url, **data) -> Manga:
        """Explicit is better than implicit."""
        manga, _ = Manga.objects.get_or_create(source_url=source_url)
        manga: Manga
        manga_already = Manga.objects.filter(source_url=source_url)
        if manga_already.exists():
            manga_already.update(**data)
            manga = manga_already.first()
            spider.logger.info(f'Updated item "{manga}"')
        else:
            manga = Manga.objects.create(
                source_url=source_url,
                **data,
            )
            spider.logger.info(f'Created item "{manga}"')
        return manga

    @classmethod
    def process_item(cls, item: dict, spider: Spider) -> dict:
        data = deepcopy(item)

        if isinstance(spider, ReadmangaListSpider) and not data.get("title", None):
            message = f"Error processing {data}: No title name was set"
            spider.logger.error(message)
            raise KeyError(message)

        source_url = data.pop("source_url")
        rss_url = data.get("rss_url", None)
        if rss_url:
            data["rss_url"] = url_prefix(spider.start_urls[0]) + rss_url

        genres = data.pop("genres", [])
        authors = data.pop("authors", [])
        illustrators = data.pop("illustrators", [])
        screenwriters = data.pop("screenwriters", [])
        translators = data.pop("translators", [])
        categories = data.pop("categories", [])

        manga = cls.get_or_create_or_update_manga(spider, source_url, **data)

        genres = bulk_get_or_create(Genre, genres)
        manga.genres.add(*genres)

        PersonRelatedToManga.save_persons(manga, PersonRole.author, authors)
        PersonRelatedToManga.save_persons(manga, PersonRole.illustrator, illustrators)
        PersonRelatedToManga.save_persons(manga, PersonRole.screenwriter, screenwriters)
        PersonRelatedToManga.save_persons(manga, PersonRole.translator, translators)

        categories = [Category.objects.get_or_create(name=category)[0] for category in categories]
        manga.categories.clear()
        manga.categories.set(categories)

        manga.save()

        return item
