from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django_extensions.db.models import TimeStampedModel


class ReprMixin:
    def __repr__(self):
        classname = self.__class__.__name__
        return f"<{classname}: {self.name}, pk: {self.pk}>"


class Author(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("author_name", unique=True)


class Category(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("category_name", unique=True)


class Translator(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("translator_name", unique=True)


class Genre(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("genre_name", unique=True)


class Manga(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("manga_name", unique=True, db_index=True)
    description = TextField("manga_description")
    status = TextField("status", null=True, blank=True)
    year = TextField("year", null=True, blank=True)
    image_url = TextField("url", default="")
    # There can be manga with no chapters, i.e. future releases
    chapters = HStoreField(null=True, blank=True)

    genres = ManyToManyField("Genre", related_name="mangas")
    categories = ManyToManyField("Category", related_name="mangas")
    author = ForeignKey("Author", related_name="mangas", on_delete=models.CASCADE, null=True, blank=True)
    translators = ManyToManyField("Translator", related_name="mangas")

    technical_params = models.JSONField(null=True, blank=True)
