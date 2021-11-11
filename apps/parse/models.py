from datetime import timedelta

from django.db import models
from django.db.models.fields import DateTimeField, FloatField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.query import QuerySet

from apps.core.abc.models import BaseModel
from apps.core.fast import FastQuerySet
from apps.core.utils import url_prefix
from apps.parse.const import SOURCE_TO_CATALOGUE_MAP


class Category(BaseModel):
    name = TextField(unique=True)


class Genre(BaseModel):
    name = TextField(unique=True)


class Person(BaseModel):
    name = TextField(unique=True)


class Author(Person):
    class AuthorManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(manga_relations__role="author")

    objects = AuthorManager()

    class Meta:
        proxy = True


class PersonRelatedToManga(models.Model):
    class Roles(models.TextChoices):
        author = "author"
        illustrator = "illustrator"
        screenwriter = "screenwriter"
        translator = "translator"

    person = ForeignKey("Person", models.CASCADE, related_name="manga_relations")
    manga = ForeignKey("Manga", models.CASCADE, related_name="person_relations")
    role = TextField(choices=Roles.choices)


class Chapter(models.Model):
    manga = ForeignKey("Manga", models.CASCADE, related_name="chapters", null=True)

    title = TextField()
    link = URLField(max_length=2000)
    number = FloatField()
    volume = FloatField()

    def __str__(self) -> str:
        return self.title


class Manga(BaseModel):
    objects = models.Manager.from_queryset(FastQuerySet)()
    NAME_FIELD = "title"

    BASE_UPDATE_FREQUENCY = timedelta(hours=1)
    IMAGE_UPDATE_FREQUENCY = timedelta(hours=8)

    title = TextField()
    alt_title = TextField(null=True, blank=True)
    rating = FloatField(default=0)
    thumbnail = URLField(max_length=2000, default="", blank=True)
    image = URLField(max_length=2000, default="", blank=True)
    description = TextField(default="", blank=True)
    status = TextField(null=True, blank=True)
    year = TextField(null=True, blank=True)
    # https://stackoverflow.com/questions/417142
    source_url = URLField(max_length=2000, unique=True)
    # There can be manga with no chapters, i.e. future releases
    rss_url = URLField(max_length=2000, null=True, blank=True)
    genres = ManyToManyField("Genre", related_name="mangas", blank=True)
    categories = ManyToManyField("Category", related_name="mangas", blank=True)
    updated_detail = DateTimeField(blank=True, null=True)
    people_related = ManyToManyField(
        "Person", through="PersonRelatedToManga", related_name="mangas"
    )

    @property
    def source(self):
        return SOURCE_TO_CATALOGUE_MAP[url_prefix(self.source_url)]

    @property
    def authors(self) -> QuerySet["Person"]:
        """For admin use only"""
        return Person.objects.filter(
            manga_relations__manga=self, manga_relations__role=PersonRelatedToManga.Roles.author
        )

    def save(self, **kwargs):
        if not self.image:
            self.image = self.thumbnail
        return super().save(**kwargs)
