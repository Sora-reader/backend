from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField


# Create your models here.
class Author(models.Model):
    name = TextField('author_name', unique=True)


class Translator(models.Model):
    name = TextField('translator_name', unique=True)


class Genre(models.Model):
    name = TextField('genre_name', unique=True)


class Category(models.Model):
    name = TextField('category_name', unique=True)


class Manga(models.Model):
    title = TextField('manga_title', unique=True)
    description = TextField('manga_description')
    status = TextField('status')
    year = TextField('year')

    genres = ManyToManyField(Genre)
    categories = ManyToManyField(Category)
    author = ForeignKey(Author, on_delete=models.CASCADE)
    translators = ManyToManyField(Translator)
