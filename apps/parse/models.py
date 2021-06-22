import re
from typing import List

from django.db import models
from django.db.models.fields import TextField, URLField
from django.db.models.fields.related import ManyToManyField

from apps.core.models import BaseModel


class Category(BaseModel):
    name = TextField(unique=True)


class Genre(BaseModel):
    name = TextField(unique=True)


class Person(BaseModel):
    name = TextField(unique=True)


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

    title = TextField(null=True, blank=True)
    alt_title = TextField(null=True, blank=True)

    # https://stackoverflow.com/questions/417142
    source_url = URLField(max_length=2000, unique=True)

    description = TextField()
    status = TextField(null=True, blank=True)
    year = TextField(null=True, blank=True)
    image_url = URLField("thumbnail url", default="")

    # There can be manga with no chapters, i.e. future releases
    chapters = models.JSONField(default=dict)

    genres = ManyToManyField("Genre", related_name="mangas")
    categories = ManyToManyField("Category", related_name="mangas")

    people_related = ManyToManyField(
        "Person", through="PersonRelatedToManga", related_name="mangas"
    )

    @property
    def source(self) -> str:
        domain = re.match(r"^http[s]?://(.*)/.*$", self.source_url).group(0)
        return self.__class__.SOURCE_MAP[domain]

    def related_people_filter(self, role: PersonRelatedToManga.Roles) -> List["Person"]:
        relations = self.person_relations.filter(role=role).all()
        return list(set(r.person for r in relations))

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
