from django.contrib import admin

from apps.core.admin import AuthorLinkMixin, BaseAdmin, ImagePreviewMixin
from apps.readmanga_parser.models import Author, Genre, Manga, TaskControl


@admin.register(Manga)
class MangaAdmin(BaseAdmin, AuthorLinkMixin, ImagePreviewMixin, admin.ModelAdmin):
    search_fields = ("title",)
    list_display = (
        "title",
        "alt_title",
        "get_image",
        "status",
        "year",
        "genres_list",
        "author_link",
    )
    list_filter = ("categories",)

    genres_list = BaseAdmin.related_string(Genre)


@admin.register(Author)
class AuthorAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Genre)
class GenreAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(TaskControl)
class TaskControlAdmin(BaseAdmin, admin.ModelAdmin):
    list_display = ("task_name", "task_status")
    list_editable = ("task_status",)
