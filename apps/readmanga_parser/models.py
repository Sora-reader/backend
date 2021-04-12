from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models.fields import TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django_extensions.db.models import TimeStampedModel


class ReprMixin:
    def __repr__(self):
        classname = self.__class__.__name__
        return f"<{classname}: {self.name}, pk: {self.pk}>"


class ScreenWriter(TimeStampedModel, ReprMixin, models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)

    name = TextField("screenwriter_name", unique=True)


class Illustrator(TimeStampedModel, ReprMixin, models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)

    name = TextField("illustrator_name", unique=True)


class Author(TimeStampedModel, ReprMixin, models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)

    name = TextField("author_name", unique=True)


class Category(TimeStampedModel, ReprMixin, models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)

    name = TextField("category_name", unique=True)


class Translator(TimeStampedModel, ReprMixin, models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)

    name = TextField("translator_name", unique=True)


class Genre(TimeStampedModel, ReprMixin, models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)

    name = TextField("genre_name", unique=True)


class Manga(TimeStampedModel, ReprMixin, models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)

    name = TextField("manga_name", null=True, blank=True)
    self_url = URLField("manga_url", max_length=1000, unique=True)
    description = TextField("manga_description")
    status = TextField("status", null=True, blank=True)
    year = TextField("year", null=True, blank=True)
    image_url = URLField("image_url", default="")
    # There can be manga with no chapters, i.e. future releases
    chapters = HStoreField(null=True, blank=True)

    genres = ManyToManyField("Genre", related_name="mangas")

    categories = ManyToManyField("Category", related_name="mangas")

    author = ForeignKey(
        "Author", related_name="mangas", on_delete=models.SET_NULL, null=True, blank=True
    )

    illustrators = ManyToManyField("Illustrator", related_name="mangas")
    screenwriters = ManyToManyField("Screenwriter", related_name="mangas")

    translators = ManyToManyField("Translator", related_name="mangas")

    technical_params = models.JSONField(default=dict)
