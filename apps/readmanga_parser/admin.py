from django.contrib import admin

from apps.core.admin import AuthorLinkMixin, BaseAdmin, ImagePreviewMixin
from apps.readmanga_parser.models import Author, Genre, Illustrator, Manga, ScreenWriter, Translator


@admin.register(Manga)
class MangaAdmin(BaseAdmin, AuthorLinkMixin, ImagePreviewMixin, admin.ModelAdmin):
    search_fields = ("title",)
    list_display = (
        "title",
        "get_image",
        "status",
        "year",
        "genres_list",
        "screenwriters_list",
        "illustrators_list",
        "author_link",
    )
    list_filter = ("categories",)

    genres_list = BaseAdmin.related_string("genres", order_by=Genre.SORT_FIELD)
    screenwriters_list = BaseAdmin.related_string("screenwriters", order_by=ScreenWriter.SORT_FIELD)
    illustrators_list = BaseAdmin.related_string("illustrators", order_by=Illustrator.SORT_FIELD)


@admin.register(Author)
class AuthorAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Genre)
class GenreAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Translator)
class TranslatorAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
