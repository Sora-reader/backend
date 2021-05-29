import easy
from django.contrib import admin
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


class BaseAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj):
        if self.__class__.fields:
            return self.__class__.fields
        fields = []
        for field in obj._meta.get_fields():
            fields.append(field)  # TODO: add logic
        return fields

    def get_list_display(self, request):
        list_display = []
        for field in self.__class__._meta.get_fields():
            if not isinstance(field, ManyToOneRel):
                if not getattr(field, "choices"):
                    list_display.append(field.name)
                else:
                    list_display.append(f"get_{field.name}_display")
        return list_display
