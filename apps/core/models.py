from django.db import models

from apps.core.abc.models import BaseModel


class TaskControl(BaseModel):
    NAME_FIELD = "name"

    status = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
