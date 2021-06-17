import logging
from typing import List, Tuple

from django.db import transaction

from apps.parse.models import Genre, Manga

logger = logging.getLogger()


@transaction.atomic
def bulk_get_or_create(cls, names: List[str]) -> Tuple:
    objects = []
    for name in names:
        objects.append(cls.objects.get_or_create(name=name))
    return tuple(obj for obj, _ in objects)


class ReadmangaPipeline:
    @staticmethod
    def process_item(item, spider):
        description = item.get("description")
        genres = item.get("genres")
        title = item.get("title")
        self_url = item.get("title_url")
        image_url = item.get("image_url")
        alt_title = item.get("alt_title")

        if not title:
            message = f"Error processing {item}: No title name was set"
            spider._logger.error(message)
            raise KeyError(message)

        genres = bulk_get_or_create(Genre, genres)

        manga, _ = Manga.objects.get_or_create(self_url=self_url)

        manga_already = Manga.objects.filter(self_url=self_url)
        if manga_already.exists():
            manga_already.update(
                title=title,
                description=description,
                image_url=image_url,
                alt_title=alt_title,
            )
            manga = manga_already.first()
            spider.logger_.info(f'Updated item "{manga}"')
        else:
            manga = Manga.objects.create(
                self_url=self_url,
                title=title,
                description=description,
                image_url=image_url,
                alt_title=alt_title,
            )
            spider.logger_.info(f'Created item "{manga}"')

        manga.genres.add(*genres)

        return item
