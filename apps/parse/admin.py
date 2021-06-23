from django.contrib import admin

from apps.core.admin import BaseAdmin, ImagePreviewMixin, RelatedField
from apps.parse.models import Author, Genre, Manga, Person


@admin.register(Manga)
class MangaAdmin(BaseAdmin, ImagePreviewMixin, admin.ModelAdmin):
    search_fields = ("title", "alt_title")
    list_display = (
        "title",
        "alt_title",
        "get_image",
        "status",
        "year",
        "authors",
        "genre_list",
    )

    authors = RelatedField(Manga.authors, html=True)
    genre_list = RelatedField(Genre)


@admin.register(Person)
class PersonAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Author)
class AuthorAdmin(PersonAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
