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


class Category(TimeStampedModel, models.Model):
    name = TextField("category_name", unique=True)


class Manga(TimeStampedModel, models.Model):
<<<<<<< HEAD

=======
>>>>>>> 6451835cb83e8493e697b0a700853de3a9169e39
    title = TextField("manga_title", unique=True)
    description = TextField("manga_description")
    status = TextField("status")
    year = TextField("year")

    genres = ManyToManyField("Genre", related_name="mangas")
    categories = ManyToManyField("Category", related_name="mangas")
    author = ForeignKey("Author", related_name="mangas", on_delete=models.CASCADE)
    translators = ManyToManyField("Translator", related_name="mangas")
