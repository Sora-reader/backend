from typing import Any, List

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
ImageList = List[str]


class ParsingSchemaOut(Schema):
    status: ParsingStatus
    data: Any


class MangaOut(ParsingSchemaOut):
    data: MangaSchema


class ChapterListOut(ParsingSchemaOut):
    data: List[ChapterSchema]


class ImageListOut(ParsingSchemaOut):
    data: List[ChapterSchema]


class MessageSchema(Schema):
    message: str


class ErrorSchema(Schema):
    error: str
