from django.db import models
from django.db.models.fields import TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from apps.core.models import BaseModel


class Author(BaseModel):
    name = TextField(unique=True)


class Category(BaseModel):
    name = TextField(unique=True)


class Genre(BaseModel):
    name = TextField(unique=True)


class Person(BaseModel):
    name = TextField(unique=True)


class Manga(BaseModel):
    NAME_FIELD = "title"

    title = TextField(null=True, blank=True)
    alt_title = TextField(null=True, blank=True)
    self_url = URLField(max_length=1000, unique=True)
    description = TextField()
    status = TextField(null=True, blank=True)
    year = TextField(null=True, blank=True)
    image_url = URLField("thumbnail url", default="")
    # There can be manga with no chapters, i.e. future releases
    chapters = models.JSONField(default=dict)

    genres = ManyToManyField("Genre", related_name="mangas")

    categories = ManyToManyField("Category", related_name="mangas")

    author = ForeignKey(
        "Author", related_name="mangas", on_delete=models.SET_NULL, null=True, blank=True
    )

    technical_params = models.JSONField(default=dict)


class PersonRole(BaseModel):
    class PersonRoles(models.TextChoices):
        ILLUSTRATOR = "Illustrator"
        SCREENWRITER = "SCREENWRITER"
        TRANSLATOR = "TRANSLATOR"

    person = models.ForeignKey(Person, models.CASCADE, related_name="persons")
    manga = models.ForeignKey(Manga, models.CASCADE, related_name="mangas")
    person_role = models.CharField(max_length=15, choices=PersonRoles.choices)
