import logging
from typing import List, Tuple

from django.db import transaction

from apps.readmanga_parser.models import Genre, Manga

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
        logger.info(item)
        description = item.get("description")
        genres = item.get("genres")
        title = item.get("title")
        self_url = item.get("title_url")
        image_url = item.get("image_url")

        if not title:
            raise KeyError("No title name was set")

        genres = bulk_get_or_create(Genre, genres)

        manga, _ = Manga.objects.get_or_create(self_url=self_url)

        manga_already = Manga.objects.filter(self_url=self_url)
        if manga_already.exists():
            manga_already.update(
                title=title,
                description=description,
                image_url=image_url,
            )
            manga = manga_already.first()
        else:
            manga = Manga.objects.create(
                self_url=self_url,
                title=title,
                description=description,
                image_url=image_url,
            )

        manga.genres.add(*genres)

        return item
