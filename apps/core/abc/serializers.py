from rest_framework import serializers

from apps.core.abc.models import BaseModel


class NameRelatedField(serializers.StringRelatedField):
    def to_representation(self, obj: BaseModel):
        if not getattr(obj, "NAME_FIELD", None):
            return super().to_representation(obj)
        return str(getattr(obj, obj.__class__.NAME_FIELD))
