import logging
from copy import deepcopy
from typing import List, Tuple, Type

from django.db import transaction
from scrapy.spiders import Spider

from apps.core.abc.models import BaseModel
from apps.manga.annotate import manga_to_annotated_dict
from apps.manga.api.schemas import ChapterListOut, ImageListOut, MangaOut
from apps.manga.models import Category, Chapter, Genre, Manga, PersonRelatedToManga, PersonRole
from apps.parse.cleaning import normalized_category_names, without_common_prefix
from apps.parse.scrapy.items import ChapterItem, ImagesItem
from apps.parse.scrapy.pipeline import CachedPipeline
from apps.parse.scrapy.spider import BaseSpider
from apps.parse.types import CacheType, ParserType, ParsingStatus
from apps.readmanga.chapter import ReadmangaChapterSpider
from apps.readmanga.image import ReadmangaImageSpider

logger = logging.getLogger("scrapy")


@transaction.atomic
def bulk_get_or_create(cls: Type[BaseModel], values: List[str], keyword: str = "name") -> Tuple:
    objects = []
    for value in values:
        objects.append(cls.objects.get_or_create(**{keyword: value}))
    return tuple(obj for obj, _ in objects)


class ReadmangaImagePipeline(CachedPipeline):
    timeout = 8 * 3600
    type = CacheType.image

    def get_cache_key(self, data: ImagesItem) -> str:
        return data["chapter_url"]

    def convert_data(self, data: ImagesItem):
        return ImageListOut(status=ParsingStatus.up_to_date, data=data["images"])

    def process(self, item: ImagesItem, spider: ReadmangaImageSpider):
        # No need to process, just save to cache
        pass


class ReadmangaChapterPipeline(CachedPipeline):
    timeout = 3600
    type = CacheType.chapter

    def get_cache_key(self, data: ChapterItem) -> str:
        return data["chapters_url"]

    def convert_data(self, data: ChapterItem):
        return ChapterListOut(
            status=ParsingStatus.up_to_date.value,
            data=data["chapters"],
        )

    def process(self, item, spider):
        # No need to process since we're overriding process_item and manually calling save_to_cache
        pass

    def process_item(self, chapters_data: ChapterItem, spider: ReadmangaChapterSpider):
        chapter_list, chapters_url = chapters_data.values()
        manga = Manga.objects.get(chapters_url=chapters_url)

        clean_chapter_titles = without_common_prefix([c["title"] for c in chapter_list])

        chapter_list = self.bulk_get_or_create(
            [
                {**c, "title": title, "manga": manga}
                for title, c in zip(clean_chapter_titles, chapter_list)
            ]
        )

        chapter = {"chapters_url": chapters_url, "chapters": chapter_list}
        self.save_to_cache(chapter, spider)

        return chapter

    @staticmethod
    @transaction.atomic
    def bulk_get_or_create(chapters: List[dict]) -> List[Chapter]:
        objects: List[Chapter, ...] = []
        for chapter in chapters:
            objects.append(Chapter.objects.get_or_create(**chapter))
        return [obj for obj, _ in objects]


class ReadmangaPipeline(CachedPipeline):
    timeout = 7 * 24 * 3600
    type = CacheType.detail

    def get_cache_key(self, data: Manga) -> str:
        return data.source_url

    def convert_data(self, data: Manga):
        return MangaOut(
            status=ParsingStatus.up_to_date.value,
            data=manga_to_annotated_dict(data),
        )

    def process(self, item, spider):
        # Once again, manual cache call
        pass

    def process_item(self, item: dict, spider: BaseSpider) -> dict:
        spider.logger.info(f"Processing item {item}")
        data = deepcopy(item)

        if spider.type == ParserType.list.value:
            message = f"Error processing {data}: No title name was set"
            spider.logger.error(message)
            raise ValueError(message)

        genres = data.pop("genres", [])
        authors = data.pop("authors", [])
        illustrators = data.pop("illustrators", [])
        screenwriters = data.pop("screenwriters", [])
        translators = data.pop("translators", [])
        categories = data.pop("categories", [])

        manga = self.get_or_create_or_update_manga(spider, data.pop("identifier"), **data)

        # TODO: move it to model, like for sav_persons use atomic transaction
        genres = bulk_get_or_create(Genre, normalized_category_names(genres))
        manga.genres.clear()
        manga.genres.add(*genres)

        categories = bulk_get_or_create(Category, normalized_category_names(categories))
        manga.categories.clear()
        manga.categories.add(*categories)

        PersonRelatedToManga.save_persons(manga, PersonRole.author, authors)
        PersonRelatedToManga.save_persons(manga, PersonRole.illustrator, illustrators)
        PersonRelatedToManga.save_persons(manga, PersonRole.screenwriter, screenwriters)
        PersonRelatedToManga.save_persons(manga, PersonRole.translator, translators)

        spider.logger.info(f"Saved manga {manga}")

        if not spider.type == ParserType.list.value:
            self.save_to_cache(manga, spider)

        return item

    @staticmethod
    def get_or_create_or_update_manga(spider: Spider, identifier, **data) -> Manga:
        """Explicit is better than implicit."""
        matching_query = Manga.objects.filter(identifier=identifier)

        if matching_query.exists():
            spider.logger.info(f"Manga exists, updating with {data}")
            matching_query.update(**data)
            manga = matching_query.first()
            spider.logger.info(f'Updated item "{manga}"')
        else:
            manga = Manga.objects.create(
                identifier=identifier,
                **data,
            )
            spider.logger.info(f'Created item "{manga}"')

        return manga
