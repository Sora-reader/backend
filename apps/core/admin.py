from typing import Callable, Optional

import easy
from django.contrib import admin
from django.db.models import Model
from django.db.models.fields import Field
from django.db.models.fields.reverse_related import ManyToOneRel
from django.utils.html import format_html


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
    @staticmethod
    def related_comma_list(
        field_name: str, order_by=None
    ) -> Callable[[admin.ModelAdmin, Model], str]:
        """
        Factory of admin list_display callables for relations. Uses NAME_FIELD as a value name

        :return: A callable which outputs relation names separated by ", "
        """

        def abc_comma_list(_, obj: Model):
            relation = getattr(obj, field_name)
            value_name = relation.model.NAME_FIELD

            return ", ".join(relation.values_list(value_name, flat=True).all())

        function = abc_comma_list
        function.__name__ = f"{field_name}_list"
        function.short_description = field_name.capitalize()
        function.admin_order_field = order_by

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
        fields = self.fields or self.model._meta.get_fields()
        for field in fields:
            field: Field
            if not isinstance(field, ManyToOneRel):
                if not getattr(field, "choices", None):
                    list_display.append(field.name)
                else:
                    list_display.append(f"get_{field.name}_display")
        return list_display
