import re
from functools import reduce

from django.db import models
from django.db.models.fields import IntegerField, TextField, URLField
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q

from apps.core.models import BaseModel


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

    person = models.ForeignKey("Person", models.CASCADE, related_name="manga_relations")
    manga = models.ForeignKey("Manga", models.CASCADE, related_name="person_relations")
    role = models.TextField(choices=Roles.choices)


class Chapter(models.Model):
    title = TextField()
    link = URLField(max_length=2000)
    number = IntegerField()

    def __str__(self) -> str:
        return self.title


class VolumesRelatedToManga(models.Model):
    manga = models.ForeignKey("Manga", models.CASCADE)
    chapter = models.ForeignKey("Chapter", models.CASCADE)
    volume = models.IntegerField()


class Manga(BaseModel):
    NAME_FIELD = "title"

    SOURCE_MAP = {
        "readmanga.live": "ReadManga",
    }

    title = TextField()
    alt_title = TextField(null=True, blank=True)
    thumbnail = URLField(max_length=2000, default="")
    image = URLField(max_length=2000, default="")
    description = TextField()
    status = TextField(null=True, blank=True)
    year = TextField(null=True, blank=True)
    # https://stackoverflow.com/questions/417142
    source_url = URLField(max_length=2000, unique=True)
    # There can be manga with no chapters, i.e. future releases
    rss_url = URLField(max_length=2000, null=True, blank=True)
    volumes = ManyToManyField("Chapter", through="VolumesRelatedToManga")
    genres = ManyToManyField("Genre", related_name="mangas")
    categories = ManyToManyField("Category", related_name="mangas")
    updated_detail = models.DateTimeField(blank=True, null=True)
    updated_chapters = models.DateTimeField(blank=True, null=True)
    people_related = ManyToManyField(
        "Person", through="PersonRelatedToManga", related_name="mangas"
    )

    @property
    def source(self) -> str:
        domain = re.match(r"^http[s]?://(.*)/.*$", self.source_url).group(1)
        return self.__class__.SOURCE_MAP[domain]

    @property
    def domain(self) -> str:
        domain = re.match(r"(^http[s]?://(.*))/.*$", self.source_url).group(1)
        return domain

    def related_people_filter(self, role: PersonRelatedToManga.Roles) -> QuerySet["Person"]:
        role_relations = self.person_relations.filter(role=role).all()
        if not role_relations:
            return Person.objects.none()
        relations = Person.objects.filter(
            reduce(
                lambda x, y: x | y,
                [Q(manga_relations__manga=relation.manga) for relation in role_relations],
            )
        )
        return relations

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
