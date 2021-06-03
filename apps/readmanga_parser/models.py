from django.db import models
from django.db.models.fields import TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from apps.core.models import BaseModel


class ScreenWriter(BaseModel):
    name = TextField("screenwriter_name", unique=True)


class Illustrator(BaseModel):
    name = TextField("illustrator_name", unique=True)


class Author(BaseModel):
    name = TextField("author_name", unique=True)


class Category(BaseModel):
    name = TextField("category_name", unique=True)


class Translator(BaseModel):
    name = TextField("translator_name", unique=True)


class Genre(BaseModel):
    name = TextField("genre_name", unique=True)


class Manga(BaseModel):
    NAME_FIELD = "title"

    title = TextField(null=True, blank=True)
    self_url = URLField(max_length=1000, unique=True)
    description = TextField()
    status = TextField("status", null=True, blank=True)
    year = TextField("year", null=True, blank=True)
    image_url = URLField("image_url", default="")
    # There can be manga with no chapters, i.e. future releases
    chapters = models.JSONField(default=dict)

    genres = ManyToManyField("Genre", related_name="mangas")

    categories = ManyToManyField("Category", related_name="mangas")

    author = ForeignKey(
        "Author", related_name="mangas", on_delete=models.SET_NULL, null=True, blank=True
    )

    illustrators = ManyToManyField("Illustrator", related_name="mangas")
    screenwriters = ManyToManyField("ScreenWriter", related_name="mangas")

    translators = ManyToManyField("Translator", related_name="mangas")

    technical_params = models.JSONField(default=dict)
