from django.db import models
from django.db.models.fields import DecimalField, FloatField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.query import QuerySet

from apps.core.abc.models import BaseModel
from apps.core.fast import FastQuerySet
from apps.core.utils import url_prefix
from apps.parse.source import SOURCE_TO_CATALOGUE_MAP


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


class PersonRole(models.TextChoices):
    author = "author"
    illustrator = "illustrator"
    screenwriter = "screenwriter"
    translator = "translator"


class PersonRelatedToManga(models.Model):
    person = ForeignKey("Person", models.CASCADE, related_name="manga_relations")
    manga = ForeignKey("Manga", models.CASCADE, related_name="person_relations")
    role = TextField(choices=PersonRole.choices)

    @staticmethod
    def save_persons(manga: "Manga", role: str, persons: list):
        people_related: PersonRelatedToManga = manga.people_related.through
        people_related.objects.filter(role=role, manga=manga).delete()
        people_related.objects.bulk_create(
            [
                people_related(  # noqa
                    person=Person.objects.get_or_create(name=person)[0],
                    manga=manga,
                    role=role,
                )
                for person in persons
            ],
            ignore_conflicts=True,
        )


class Chapter(BaseModel):
    NAME_FIELD = "title"

    manga = ForeignKey("Manga", models.CASCADE, related_name="chapters", null=True)

    title = TextField()
    link = URLField(max_length=2000)
    number = FloatField()
    volume = FloatField()


class Manga(BaseModel):
    class Meta:
        verbose_name = "Manga"
        verbose_name_plural = "Manga"

    objects = models.Manager.from_queryset(FastQuerySet)()
    NAME_FIELD = "title"

    title = TextField()
    # Identifier for source site. Can be a direct ID or a hash
    identifier = TextField()

    rating = DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
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
    people_related = ManyToManyField(
        "Person", through="PersonRelatedToManga", related_name="mangas"
    )

    @property
    def source(self):
        return SOURCE_TO_CATALOGUE_MAP[url_prefix(self.source_url)]

    def save(self, **kwargs):
        if not self.image:
            self.image = self.thumbnail
        return super().save(**kwargs)

    @property
    def authors(self) -> QuerySet[Author]:
        return Author.objects.filter(manga_relations__manga=self)
