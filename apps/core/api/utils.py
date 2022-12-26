from typing import List, Type

from django.http import Http404

from apps.core.abc.models import BaseModel
from apps.core.api.schemas import ErrorSchema, MessageSchema


def sora_schema(schema):
    return {200: schema, 400: ErrorSchema, 425: MessageSchema}


def get_model_or_404(cls: Type[BaseModel], pk, prefetch: List[str] = None):
    obj = cls.objects.filter(pk=pk).prefetch_related(*(prefetch or [])).first()
    if not obj:
        raise Http404(f"No {cls.__name__.lower()} found")
    return obj
