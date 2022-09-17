from ninja import ModelSchema

from apps.manga.models import Manga


class MangaOut(ModelSchema):
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
