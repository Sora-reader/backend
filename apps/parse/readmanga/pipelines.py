from copy import deepcopy
from typing import List, Tuple

from django.db import transaction
from scrapy.spiders import Spider

from apps.parse.models import Genre, Manga
from apps.parse.readmanga.images import ReadmangaImageSpider


@transaction.atomic
def bulk_get_or_create(cls, names: List[str]) -> Tuple:
    objects = []
    for name in names:
        objects.append(cls.objects.get_or_create(name=name))
    return tuple(obj for obj, _ in objects)


class ReadmangaImagePipeline:
    @staticmethod
    def process_item(item: dict, spider: ReadmangaImageSpider):
        spider.redis_client.rpush(spider.start_urls[0], *item)


class ReadmangaPipeline:
    @staticmethod
    def process_item(item: dict, spider: Spider):
        # TODO: Add person/categories/chapters saving
        # P.S. look at the bottom
        data = deepcopy(item)

        title = data.pop("title")
        genres = data.pop("genres")
        source_url = data.pop("source_url")

        if not title:
            message = f"Error processing {data}: No title name was set"
            spider.logger.error(message)
            raise KeyError(message)

        genres = bulk_get_or_create(Genre, genres)

        manga, _ = Manga.objects.get_or_create(source_url=source_url)
        manga: Manga
        manga_already = Manga.objects.filter(source_url=source_url)
        if manga_already.exists():
            manga_already.update(title=title, **data)
            manga = manga_already.first()
            spider.logger.info(f'Updated item "{manga}"')
        else:
            manga = Manga.objects.create(
                title=title,
                source_url=source_url,
                **data,
            )
            spider.logger.info(f'Created item "{manga}"')

        manga.genres.add(*genres)

        return item


# def save_detailed_manga_info(
#     manga: Manga,
#     **kwargs,
# ) -> None:
#     if manga is None:
#         return

#     data = deepcopy(kwargs)

#     authors = data.pop("authors", [])
#     illustrators = data.pop("illustrators", [])
#     screenwriters = data.pop("screenwriters", [])
#     translators = data.pop("translators", [])
#     categories = data.pop("categories", [])

#     save_persons(manga, PersonRelatedToManga.Roles.author, authors)
#     save_persons(manga, PersonRelatedToManga.Roles.illustrator, illustrators)
#     save_persons(manga, PersonRelatedToManga.Roles.screenwriter, screenwriters)
#     save_persons(manga, PersonRelatedToManga.Roles.translator, translators)

#     categories = [Category.objects.get_or_create(name=category)[0] for category in categories]

#     manga.categories.clear()
#     manga.categories.set(categories)
#     data["updated_detail"] = timezone.now()
#     data["rss_url"] = url_prefix(manga.source_url) + data.pop("rss_url", "")
#     Manga.objects.filter(pk=manga.pk).update(**data)
