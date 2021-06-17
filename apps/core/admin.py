from typing import Callable, Dict, Optional, Tuple, Type, Union

import easy
from django.contrib import admin
from django.db.models import Model
from django.db.models.fields import Field
from django.utils.html import format_html

from apps.core.models import BaseModel, TaskControl


class AuthorLinkMixin:
    @easy.smart(short_description="Author", admin_order_field="author__name")
    def author_link(self, obj) -> str:
        return (
            format_html(f"<a href='{obj.author.admin_url}'>{obj.author.name}</a>")
            if obj.author
            else "-"
        )


class ImagePreviewMixin:
    @easy.smart(__name__="Image")
    def get_image(self, obj):
        style = "max-height: 100px; border-radius: 3px;"
        return format_html(f"<img src='{obj.image_url}' style='{str(style)}' />")


class ManyRelatedManager:
    pass


class BaseAdmin(admin.ModelAdmin):
    # Cached key for relations like {(ModelFrom, ModelTo): 'model_too'}
    # Where ModelFrom().model_too is a relation
    RELATED_CACHE: Dict[Tuple, str] = {}

    @classmethod
    def related_string(
        cls,
        field_or_model: Union[str, Type[BaseModel]],
        *,
        name_field: Optional[str] = None,
        separator: str = ", ",
        on_empty: str = "-",
        additional_filter: Optional[dict] = None,
    ) -> Callable[[admin.ModelAdmin, Model], str]:
        """
        Factory of admin list_display callables for relations.

        :return: A callable which outputs relation names separated by provided separator
        """

        field_type = type(field_or_model)
        if isinstance(field_type, (str, type(BaseModel))):
            raise ValueError("One of field_name or model must be provided")

        def abc_related_string(_, obj: Model):
            relation = None
            if field_type is str:
                relation = getattr(obj, field_or_model)
            else:
                # Cache key is the tuple of relation (ModelFrom, ModelTo)
                cache_key = (type(obj), field_or_model)
                cached_relation = cls.RELATED_CACHE.get(cache_key, None)
                if cached_relation:
                    relation = getattr(obj, cached_relation)
                else:
                    # Search for all fields, find first relation matching model and add it to cache
                    for field in obj._meta.get_fields():
                        if getattr(field, "related_model", None) is field_or_model:
                            relation = getattr(obj, field.attname)
                            cls.RELATED_CACHE[cache_key] = field.attname
                            break

            if not relation:
                raise ValueError(f"Can't find relation for {field_or_model} from {obj}")
            value_name = name_field or relation.model.NAME_FIELD

            filter_ = additional_filter or {}
            return (
                # flat values_list returns a query with only names, not tuples of values
                # works only for values_list with 1 argument
                separator.join(relation.filter(**filter_).values_list(value_name, flat=True).all())
                or on_empty
            )

        function = abc_related_string
        if field_type is str:
            function.short_description = field_or_model.capitalize()
        else:
            function.short_description = field_or_model._meta.verbose_name_plural.capitalize()

        return function

    def get_fields(self, request, obj: Optional[Model] = None):
        if self.fields:
            return self.fields
        if not obj:
            return super().get_fields(request, obj)
        fields = []
        for field in obj._meta.get_fields():
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
        for field in obj._meta.get_fields():
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
