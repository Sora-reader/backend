from typing import List

from ninja import ModelSchema, Schema

from apps.manga.models import Chapter, Manga
from apps.parse.types import ParsingStatus


class MangaSchema(ModelSchema):
    authors: List[str]
    genres: List[str]

    class Config:
        model = Manga
        model_fields = (
            "id",
            # "source",
            "source_url",
            "title",
            "alt_title",
            "rating",
            "thumbnail",
            "image",
            "description",
            # "screenwriters",
            # "illustrators",
            # "translators",
            # "categories",
            "status",
            "year",
            "modified",
        )

    @staticmethod
    def resolve_genres(obj: Manga):
        return [g.name for g in obj.genres.all()]

    @staticmethod
    def resolve_authors(obj: Manga):
        return [g.name for g in obj.authors]


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
