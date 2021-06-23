import logging
from copy import deepcopy
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
        data = deepcopy(item)

        title = data.pop("title")
        genres = data.pop("genres")
        source_url = data.pop("source_url")

        if not title:
            message = f"Error processing {data}: No title name was set"
            spider._logger.error(message)
            raise KeyError(message)

        genres = bulk_get_or_create(Genre, genres)

        manga, _ = Manga.objects.get_or_create(source_url=source_url)

        manga_already = Manga.objects.filter(source_url=source_url)
        if manga_already.exists():
            manga_already.update(title=title, **data)
            manga = manga_already.first()
            spider.logger_.info(f'Updated item "{manga}"')
        else:
            manga = Manga.objects.create(
                title=title,
                source_url=source_url,
                **data,
            )
            spider.logger_.info(f'Created item "{manga}"')

        manga.genres.add(*genres)

        return item
