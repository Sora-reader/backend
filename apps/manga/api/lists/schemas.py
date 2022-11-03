from typing import List

from ninja import ModelSchema, Schema

from apps.manga.api.schemas import MangaSchema
from apps.manga.models import SaveList


class SaveListOut(ModelSchema):
    mangas: List[MangaSchema] = []

    class Config:
        model = SaveList
        model_fields = [
            "id",
            "name",
        ]


class SaveListEditOut(Schema):
    count: int
