from django.contrib import admin

from apps.core.admin_mixins import AuthorLinkMixin, ImagePreviewMixin
from apps.readmanga_parser.models import (
    Translator,
    Author,
    Manga,
    Genre,
)


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin, AuthorLinkMixin, ImagePreviewMixin):
    search_fields = ('name',)
    list_display = (
        'name',
        'status',
        'year',
        'genres_list',
        'genres_list',
        'screenwriters_list',
        'illustrators_list',
        'get_image'
    )
    list_filter = ('categories',)

    def genres_list(self, obj):
        return ",\n".join([g.name for g in obj.genres.all()])

    def screenwriters_list(self, obj):
        return ",\n".join([s.name for s in obj.screenwriters.all()])

    def illustrators_list(self, obj):
        return ",\n".join([i.name for i in obj.illustrators.all()])

    genres_list.short_description = 'Genres'
    screenwriters_list.short_description = 'Screenwriters'
    illustrators_list.short_description = 'Illustrators'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
