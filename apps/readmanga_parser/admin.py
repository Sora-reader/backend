import easy
from django.contrib import admin

from apps.core.admin import AuthorLinkMixin, BaseAdmin, ImagePreviewMixin
from apps.readmanga_parser.models import Author, Genre, Manga, Translator


@admin.register(Manga)
class MangaAdmin(BaseAdmin, AuthorLinkMixin, ImagePreviewMixin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "get_image",
        "status",
        "year",
        "genres_list",
        "genres_list",
        "screenwriters_list",
        "illustrators_list",
        "author_link",
    )
    list_filter = ("categories",)

    @easy.smart(short_description="Genres")
    def genres_list(self, obj):
        return ",\n".join([g.name for g in obj.genres.all()])

    @easy.smart(short_description="Screenwriters")
    def screenwriters_list(self, obj):
        return ",\n".join([s.name for s in obj.screenwriters.all()])

    @easy.smart(short_description="Illustrators")
    def illustrators_list(self, obj):
        return ",\n".join([i.name for i in obj.illustrators.all()])


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
