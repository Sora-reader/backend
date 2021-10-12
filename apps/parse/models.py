import re
from datetime import timedelta

from django.db import models
from django.db.models.fields import FloatField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.query import QuerySet

from apps.core.abc.models import BaseModel
from apps.core.fast import FastQuerySet


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
    title = TextField()
    link = URLField(max_length=2000)
    number = FloatField()
    volume = FloatField()

    def __str__(self) -> str:
        return self.title


class Manga(BaseModel):
    objects = models.Manager.from_queryset(FastQuerySet)()
    NAME_FIELD = "title"

    UPDATED_DETAIL_FREQUENCY = timedelta(hours=1)
    UPDATED_CHAPTER_FREQUENCY = timedelta(hours=1)
    UPDATED_IMAGE_FREQUENCY = timedelta(hours=8)

    SOURCE_MAP = {
        "https://readmanga.io": "Readmanga",
        "https://mangalib.me": "Mangalib",
    }

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
    chapters = ManyToManyField("Chapter", blank=True)
    genres = ManyToManyField("Genre", related_name="mangas", blank=True)
    categories = ManyToManyField("Category", related_name="mangas", blank=True)
    updated_detail = models.DateTimeField(blank=True, null=True)
    updated_chapters = models.DateTimeField(blank=True, null=True)
    people_related = ManyToManyField(
        "Person", through="PersonRelatedToManga", related_name="mangas"
    )

    @property
    def url_prefix(self) -> str:
        return re.match(r"(^http[s]?://(.*))/.*$", self.source_url).group(1)

    @property
    def source(self) -> str:
        return self.__class__.SOURCE_MAP[self.url_prefix]

    def related_people_filter(self, role: PersonRelatedToManga.Roles) -> QuerySet["Person"]:
        return Person.objects.filter(manga_relations__manga=self, manga_relations__role=role)

    @property
    def authors(self):
        return self.related_people_filter(role=PersonRelatedToManga.Roles.author)

    @property
    def screenwriters(self):
        return self.related_people_filter(role=PersonRelatedToManga.Roles.screenwriter)

    @property
    def illustrators(self):
        return self.related_people_filter(role=PersonRelatedToManga.Roles.illustrator)

    @property
    def translators(self):
        return self.related_people_filter(role=PersonRelatedToManga.Roles.translator)

    def save(self, **kwargs):
        if not self.image:
            self.image = self.thumbnail
        return super().save(**kwargs)


# Manga.objects.map(source=("source_url__startswith", Manga.SOURCE_MAP)).m2m_agg(
#     authors=("person_relations__person__name", Q(person_relations__role="author")),
#     screenwriters=("person_relations__person__name", Q(person_relations__role="screenwriter")),
#     illustrators=("person_relations__person__name", Q(person_relations__role="illustrator")),
#     translators=("person_relations__person__name", Q(person_relations__role="translator")),
#     genres="genres__name",
#     categories="categories__name",
# ).all()[:1].fast_values(
#     "id",
#     "source",
#     "source_url",
#     "title",
#     "alt_title",
#     "rating",
#     "thumbnail",
#     "image",
#     "description",
#     "authors",
#     "screenwriters",
#     "illustrators",
#     "translators",
#     "categories",
#     "genres",
#     "status",
#     "year",
#     "updated_chapters",
#     "updated_detail",
# )
