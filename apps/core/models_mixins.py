from django.db import models
from django_extensions.db.models import TimeStampedModel


class ReprMixin:
    def __repr__(self):
        classname = self.__class__.__name__
        return f"<{classname}: {self.name}, pk: {self.pk}>"


class BaseModel(TimeStampedModel, models.Model, ReprMixin):
    class Meta:
        abstract = True
