from typing import Any, Union

from apps.readmanga_parser.models import Manga


def get_or_none(cls, **kwargs) -> Union[Any, None]:
    try:
        return cls.objects.filter(**kwargs).first()
    except cls.DoesNotExist:
        return None


class MangaQuery:
    @staticmethod
    def get_manga_by_title(title: str) -> Union[Manga, None]:
        return get_or_none(Manga, name__icontains=title)
