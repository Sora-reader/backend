from functools import cached_property
from typing import Dict, Optional, Tuple, Type, Union

import easy
from django.contrib import admin
from django.db.models import Model
from django.db.models.fields import Field
from django.utils.html import format_html

from apps.core.models import BaseModel, TaskControl
from apps.parse.models import Manga


class ImagePreviewMixin:
    @easy.smart(__name__="Image")
    def get_image(self, obj: Manga):
        style = "max-height: 100px; border-radius: 3px;"
        return format_html(f"<img src='{obj.image_url}' style='{str(style)}' />")


class RelatedField:
    """Factory of admin list_display callables for relations."""

    # Cached key for relations like {(ModelFrom, ModelTo): 'model_too'}
    # Where ModelFrom().model_too is a relation
    RELATED_CACHE: Dict[Tuple, str] = {}

    def __init__(
        self,
        lookup: Union[str, property, Type[BaseModel]],
        *,
        html: bool = False,
        name_field: Optional[str] = None,
        separator: str = ", ",
        on_empty: str = "-",
        additional_filter: Optional[dict] = None,
        description: Optional[str] = "Related field",
    ) -> None:
        self.lookup = lookup
        if not (
            self.lookup_type is type(BaseModel)
            or self.lookup_type is str
            or self.lookup_type is property
        ):
            raise ValueError(f"lookup must be str/property=>QuerySet/Model. {self.lookup_type}")

        self.html = html
        self.name_field = name_field
        self.separator = separator
        self.on_empty = on_empty
        self.additional_filter = additional_filter
        self.description = description

        self.obj = None

    @cached_property
    def lookup_type(self):
        return type(self.lookup)

    @cached_property
    def short_description(self) -> str:
        if self.lookup_type is str:
            return self.lookup.capitalize()
        elif self.lookup_type is type(BaseModel):
            return self.lookup._meta.verbose_name_plural.capitalize()
        return self.description

    def get_queryset(self) -> list:
        queryset = None
        if self.lookup_type is property:
            queryset = self.lookup.__get__(self.obj)
        elif self.lookup_type is str:
            queryset = getattr(self.obj, self.lookup)
        else:
            # Cache key is the tuple of relation (ModelFrom, ModelTo)
            cache_key = (type(self.obj), self.lookup)
            cached_relation = self.__class__.RELATED_CACHE.get(cache_key, None)
            if cached_relation:
                queryset = getattr(self.obj, cached_relation)
            else:
                # Search for all fields, find first relation matching model and add it to cache
                for field in self.obj._meta.get_fields():
                    if getattr(field, "related_model", None) is self.lookup:
                        queryset = getattr(self.obj, field.attname)
                        self.__class__.RELATED_CACHE[cache_key] = field.attname
                        break

            if not queryset:
                raise ValueError(f"Can't find relation for {self.lookup} from {self.obj}")
        return queryset

    def get_values(self):
        queryset = self.get_queryset()
        filter_ = self.additional_filter or {}

        if self.lookup_type is not property:
            value_name = self.name_field or queryset.model.NAME_FIELD
        else:
            value_name = self.name_field or None

        if self.lookup_type is not property and not self.html:
            return queryset.filter(**filter_).values_list(value_name, flat=True).all(), value_name
        return queryset.filter(**filter_).all(), value_name

    def format_values(self, values) -> str:
        if self.lookup_type is property:
            if self.html:
                output = format_html(self.separator.join([self.to_html(value) for value in values]))
            elif self.value_name:
                output = self.separator.join([getattr(value, self.value_name) for value in values])
        else:
            output = self.separator.join(values)
        return output or self.on_empty

    def __call__(self, obj: BaseModel):
        self.obj = obj
        data = self.get_values()
        values, self.value_name = data
        return self.format_values(values)

    def to_html(self, obj: BaseModel) -> str:
        if not self.value_name:
            return f"<a href='{obj.admin_url}'>{obj}</a>"
        string = getattr(obj, self.value_name)
        return f"<a href='{obj.admin_url}'>{string}</a>"


class BaseAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj: Optional[Model] = None):
        if self.fields:
            return self.fields
        if not obj:
            return super().get_fields(request, obj)
        fields = []
        for field in obj._meta.fields:
            field: Field
            if not field.editable or field.primary_key:
                continue
            fields.append(field.name)
        return fields

    def get_readonly_fields(self, request, obj: Optional[Model] = None):
        if self.readonly_fields:
            return self.readonly_fields
        if not obj:
            return super().get_readonly_fields(request, obj)
        fields = self.get_fields(request, obj)
        readonly = []
        for field in obj._meta.fields:
            field: Field
            if not field.editable and field.name in fields:
                readonly.append(field.name)
        return readonly

    def get_list_display(self, request):
        if self.list_display:
            return self.list_display
        list_display = []
        self.model: Model
        fields = self.fields or self.model._meta.fields
        for field in fields:
            field: Field
            if not getattr(field, "choices", None):
                list_display.append(field.name)
            else:
                list_display.append(f"get_{field.name}_display")
        return list_display


@admin.register(TaskControl)
class TaskControlAdmin(BaseAdmin, admin.ModelAdmin):
    list_display = ("task_name", "task_status")
    list_editable = ("task_status",)
