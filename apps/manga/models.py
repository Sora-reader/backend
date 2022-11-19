from django.db import models
from django.db.models import Q
from django.db.models.fields import CharField, DecimalField, FloatField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.query import QuerySet

from apps.core.abc.models import BaseModel
from apps.core.fast import FastQuerySet
from apps.core.utils import url_prefix
from apps.parse.catalogue import Catalogue


class OptionalUser(models.Model):
    class Meta:
        abstract = True

    @staticmethod
    def get_optional_user_constraint(prefix: str):
        # There's also a unique index with the name of save_list_user_name_unique
        # Django doesn't support those for now, so it's just a migrations with raw SQL
        return models.CheckConstraint(
            check=Q(user__isnull=False) | Q(session__isnull=False), name=f"{prefix}not_both_null"
        )

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)
    session = models.TextField(blank=True, null=True)


class Category(BaseModel):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

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


class Bookmark(BaseModel, OptionalUser):
    class Meta:
        constraints = [OptionalUser.get_optional_user_constraint("bookmark_")]

    manga = models.ForeignKey(
        "Manga", related_name="bookmarks", on_delete=models.CASCADE, blank=False, null=False
    )
    chapter = models.ForeignKey(
        "Chapter", related_name="bookmarks", on_delete=models.CASCADE, blank=False, null=False
    )


class Manga(BaseModel):
    class Meta:
        verbose_name = "Manga"
        verbose_name_plural = "Manga"

    objects = models.Manager.from_queryset(FastQuerySet)()
    NAME_FIELD = "title"

    title = CharField(max_length=512, null=True, blank=True)

    # Identifier for source site. Can be a direct ID or a hash
    identifier = CharField(max_length=1024, null=True, blank=True)

    rating = DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
    thumbnail = URLField(max_length=2000, default="", blank=True)
    image = URLField(max_length=2000, default="", blank=True)
    description = TextField(default="", blank=True)
    status = CharField(max_length=255, null=True, blank=True)
    year = CharField(max_length=255, null=True, blank=True)

    # https://stackoverflow.com/questions/417142
    source_url = URLField(max_length=2000, unique=True)
    # There can be manga with no chapters, i.e. future releases
    chapters_url = URLField(max_length=2000, null=True, blank=True)

    genres = ManyToManyField("Genre", related_name="mangas", blank=True)
    categories = ManyToManyField("Category", related_name="mangas", blank=True)
    people_related = ManyToManyField(
        "Person", through="PersonRelatedToManga", related_name="mangas"
    )

    @property
    def source(self):
        return Catalogue.from_source(url_prefix(self.source_url))

    def save(self, **kwargs):
        if not self.image:
            self.image = self.thumbnail
        if self.source == "mangachan":
            self.chapters_url = self.source_url
        return super().save(**kwargs)

    @property
    def authors(self) -> QuerySet[Author]:
        return Author.objects.filter(manga_relations__manga=self)


class SaveListMangaThrough(models.Model):
    class Meta:
        unique_together = ("save_list", "manga")
        # TODO: Add constraint for manga to be only in 1 of user's lists

    save_list = ForeignKey("SaveList", models.CASCADE)
    manga = ForeignKey("Manga", models.CASCADE)


class SaveListNameChoices(models.TextChoices):
    reading = "Читаю"
    favorite = "Избранные"
    read_later = "Читать позже"
    dropped = "Брошенные"


class SaveList(BaseModel, OptionalUser):
    class Meta:
        constraints = [OptionalUser.get_optional_user_constraint("")]

    name = models.TextField(choices=SaveListNameChoices.choices, null=False, blank=False)

    mangas = models.ManyToManyField("Manga", related_name="lists", through=SaveListMangaThrough)
