from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel


class ReprMixin:
    def __repr__(self):
        classname = self.__class__.__name__
        return f"<{classname}: {self.name}, pk: {self.pk}>"


class BaseModel(TimeStampedModel, ReprMixin, models.Model):
    class Meta:
        abstract = True

    @property
    def admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=(self.pk,))
