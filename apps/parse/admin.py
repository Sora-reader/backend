from django.contrib import admin

from apps.core.admin import BaseAdmin, ImagePreviewMixin
from apps.parse.models import Genre, Manga, Person


@admin.register(Manga)
class MangaAdmin(BaseAdmin, ImagePreviewMixin, admin.ModelAdmin):
    search_fields = ("title", "alt_title")
    list_display = (
        "title",
        "alt_title",
        "get_image",
        "status",
        "year",
        "genres_list",
        "authors",
    )

    authors = BaseAdmin.related_string(Manga.authors, short_description="Authors", html=True)
    genres_list = BaseAdmin.related_string(Genre)


@admin.register(Person)
class PersonAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Genre)
class GenreAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
