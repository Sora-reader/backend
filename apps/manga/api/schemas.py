from ninja import ModelSchema, Schema

from apps.manga.models import Chapter, Manga
from apps.parse.types import ParsingStatus


class MangaSchema(ModelSchema):
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
            # "authors",
            # "screenwriters",
            # "illustrators",
            # "translators",
            # "genres",
            # "categories",
            "status",
            "year",
            "modified",
        )


class ChapterSchema(ModelSchema):
    class Config:
        model = Chapter
        model_fields = "__all__"


class MangaDetail(Schema):
    status: ParsingStatus
    data: MangaSchema


class ChapterOut(Schema):
    status: ParsingStatus
    data: ChapterSchema
