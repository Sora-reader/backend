import re

from django.db import models
from django.db.models.fields import FloatField, TextField, URLField
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet

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


class Manga(BaseModel):
    NAME_FIELD = "title"

    SOURCE_MAP = {
        "readmanga.live": "ReadManga",
    }

    title = TextField()
    alt_title = TextField(null=True, blank=True)
    rating = FloatField(default=0)
    thumbnail = URLField(max_length=2000, default="")
    image = URLField(max_length=2000, default="")
    description = TextField()
    status = TextField(null=True, blank=True)
    year = TextField(null=True, blank=True)
    # https://stackoverflow.com/questions/417142
    source_url = URLField(max_length=2000, unique=True)
    # There can be manga with no chapters, i.e. future releases
    volumes = models.JSONField(default=dict)
    genres = ManyToManyField("Genre", related_name="mangas")
    categories = ManyToManyField("Category", related_name="mangas")

    people_related = ManyToManyField(
        "Person", through="PersonRelatedToManga", related_name="mangas"
    )

    @property
    def source(self) -> str:
        domain = re.match(r"^http[s]?://(.*)/.*$", self.source_url).group(1)
        return self.__class__.SOURCE_MAP[domain]

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
