# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import List, Tuple

from django.db import transaction

from apps.readmanga_parser.models import Author, Genre, Manga, Translator


@transaction.atomic
def bulk_get_or_create(cls, names: List[str]) -> Tuple:
    objects = []
    for name in names:
        objects.append(cls.objects.get_or_create(name=name))
    return (obj for obj, _ in objects)


class ReadmangaPipeline:
    def process_item(self, item, spider):
        print(item)
        description = item.get("description")
        genres = item.get("genres")
        title = item.get("title")
        image = item.get("image_url")

        if not title:
            raise KeyError("No title name was set")

        genres = bulk_get_or_create(Genre, genres)
        manga, _ = Manga.objects.get_or_create(title=title,
                                               description=description,
                                               image_url=image,
                                               )
        manga.genres.add(*genres)

        return item
