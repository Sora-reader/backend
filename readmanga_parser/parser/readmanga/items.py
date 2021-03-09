# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from readmanga_parser.models import (
    Author,
    Category,
    Genre,
    Manga,
    Status,
    Translator
)
from scrapy_djangoitem import DjangoItem


class AuthorItem(DjangoItem):
    django_model = Author


class CategoryItems(DjangoItem):
    django_model = Category


class StatusItem(DjangoItem):
    django_model = Status


class GenreItem(DjangoItem):
    django_model = Genre


class TranslatorItem(DjangoItem):
    django_model = Translator


class MangaItem(DjangoItem):
    django_model = Manga
