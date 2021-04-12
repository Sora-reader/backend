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
    return (obj for obj, _ in objects)


class ReadmangaPipeline:
    def process_item(self, item, spider):
        logger.info(item)
        description = item.get("description")
        genres = item.get("genres")
        title = item.get("title")
        title_url = item.get("title_url")
        image = item.get("image_url")

        if not title:
            raise KeyError("No title name was set")

        genres = bulk_get_or_create(Genre, genres)
        manga, _ = Manga.objects.get_or_create(
            name=title, description=description, image_url=image, self_url=title_url
        )
        manga.genres.add(*genres)

        return item
