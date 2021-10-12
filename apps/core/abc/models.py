from django.db import models
from django.db.models.fields import related_descriptors
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel, models.Model):
    NAME_FIELD = "name"
    SORT_FIELD = NAME_FIELD

    class Meta:
        abstract = True

    @property
    def admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=(self.pk,))

    @classmethod
    def is_field(cls, field: str):
        return type(getattr(cls, field, None)).__name__ in vars(related_descriptors).keys()

    def __str__(self):
        return f"{getattr(self, self.__class__.NAME_FIELD, '')} #{self.pk}"

    def __repr__(self):
        classname = self.__class__.__name__
        return f"<{classname}: {getattr(self, self.__class__.NAME_FIELD, '')}, pk: {self.pk}>"
