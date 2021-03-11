from typing import Any, Union
from readmanga_parser.models import Manga


def get_or_none(cls, **kwargs) -> Union[Any, None]:
    try:
        return cls.objects.get(**kwargs)
    except cls.DoesNotExist:
        return None


class MangaQuery:
    def get_manga_by_title(self, title: str) -> Union[Manga, None]:
        return get_or_none(Manga, title=title)

    def get_manga_by_pk(self, _id: int) -> Union[Manga, None]:
        return get_or_none(Manga, id=_id)
