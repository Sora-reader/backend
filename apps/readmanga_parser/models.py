from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django_extensions.db.models import TimeStampedModel


class Author(TimeStampedModel, models.Model):
    name = TextField("author_name", unique=True)


class Translator(TimeStampedModel, models.Model):
    name = TextField("translator_name", unique=True)


class Genre(TimeStampedModel, models.Model):
    name = TextField("genre_name", unique=True)


class Manga(TimeStampedModel, models.Model):
    title = TextField("manga_title", unique=True, db_index=True)
    description = TextField("manga_description")
    status = TextField("status", null=True, blank=True)
    year = TextField("year", null=True, blank=True)
    image_url = TextField("url", default="")
    # There can be manga with no chapters, i.e. future releases
    chapters = HStoreField(null=True, blank=True)

    genres = ManyToManyField("Genre", related_name="mangas")
    author = ForeignKey("Author", related_name="mangas", on_delete=models.CASCADE, null=True, blank=True)
    translators = ManyToManyField("Translator", related_name="mangas")
