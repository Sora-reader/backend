from django.db import models
from django.db.models.fields import TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from apps.core.models_mixins import ReprMixin


class ScreenWriter(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("screenwriter_name", unique=True)


class Illustrator(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("illustrator_name", unique=True)


class Author(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("author_name", unique=True)

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=(self.pk,))


class Category(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("category_name", unique=True)


class Translator(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("translator_name", unique=True)


class Genre(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("genre_name", unique=True)


class Manga(TimeStampedModel, ReprMixin, models.Model):
    name = TextField("manga_name", null=True, blank=True)
    self_url = URLField("manga_url", max_length=1000, unique=True)
    description = TextField("manga_description")
    status = TextField("status", null=True, blank=True)
    year = TextField("year", null=True, blank=True)
    image_url = URLField("image_url", default="")
    # There can be manga with no chapters, i.e. future releases
    chapters = models.JSONField(default=dict)

    genres = ManyToManyField("Genre", related_name="mangas")

    categories = ManyToManyField("Category", related_name="mangas")

    author = ForeignKey(
        "Author", related_name="mangas", on_delete=models.SET_NULL, null=True, blank=True
    )

    illustrators = ManyToManyField("Illustrator", related_name="mangas")
    screenwriters = ManyToManyField("Screenwriter", related_name="mangas")

    translators = ManyToManyField("Translator", related_name="mangas")

    technical_params = models.JSONField(default=dict)
