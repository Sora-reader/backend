from typing import List

from ninja import ModelSchema, Schema

from apps.manga.models import Chapter, Manga
from apps.parse.types import ParsingStatus

# Models


class MangaSchema(ModelSchema):
    source: str
    authors: List[str]
    screenwriters: List[str]
    illustrators: List[str]
    translators: List[str]
    categories: List[str]
    genres: List[str]

    class Config:
        model = Manga
        model_fields = (
            "id",
            "source_url",
            "rss_url",
            "title",
            "rating",
            "thumbnail",
            "image",
            "description",
            "status",
            "year",
            "modified",
        )


class ChapterSchema(ModelSchema):
    class Config:
        model = Chapter
        model_fields = [
            "id",
            "title",
            "volume",
            "number",
            "link",
        ]


ImageSchema = str

# Modifications and collections

MangaList = List[MangaSchema]


class MangaOut(Schema):
    status: ParsingStatus
    data: MangaSchema


class ChapterListOut(Schema):
    status: ParsingStatus
    data: List[ChapterSchema]


class ImageListOut(Schema):
    __root__: List[ImageSchema]

    class Config:
        arbitrary_types_allowed = True
