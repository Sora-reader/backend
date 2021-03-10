# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import List, Tuple
from itemadapter import ItemAdapter
from readmanga_parser.models import (
    Author,
    Genre,
    Manga,
    Translator
)
from django.db import transaction


@transaction.atomic
def bulk_get_or_create(cls, names: List[str]) -> Tuple:
    objects = []
    for name in names:
        objects.append(
            cls.objects.get_or_create(name=name))
    return (obj for obj, _ in objects)


class ReadmangaPipeline:
    def process_item(self, item, spider):
        author = item.get('author')
        description = item.get('description')
        genres = item.get('genres')
        name = item.get('name')
        translators = item.get('translators')
        year = item.get('year')

        author, _ = Author.objects.get_or_create(name=author)
        genres = bulk_get_or_create(Genre, genres)
        translators = bulk_get_or_create(Translator, translators)
        manga = Manga.objects.get_or_create(title=name,
                                    description=description,
                                    year=year,
                                    author=author)
        print(genres)
        manga.genres.add(*genres)
        manga.translators.add(*translators)

        return item
