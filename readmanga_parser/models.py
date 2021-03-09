from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField

# Create your models here.

class Author(models.Model):
    name = TextField('author_name')


class Translator(models.Model):
    name = TextField('translator_name')


class Genre(models.Model):
    name = TextField('genre_name')


class Category(models.Model):
    name = TextField('category_name')


class Status(models.Model):
    name = TextField('status_name')


class Manga(models.Model):
    title = TextField('manga_title')
    genres = ManyToManyField(Genre)
    categories = ManyToManyField(Category)
    authors = ManyToManyField(Author)
    translators = ManyToManyField(Translator)
    status = ForeignKey(Status, on_delete=models.CASCADE)
