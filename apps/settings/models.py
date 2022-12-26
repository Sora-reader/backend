from django.contrib.postgres.fields import JSONField
from django.db.models import CASCADE, ForeignKey

from apps.core.abc.models import BaseModel


class UserPreferences(BaseModel):
    user = ForeignKey("auth.User", null=False, blank=False, on_delete=CASCADE)
    catalogues = JSONField(default={})
