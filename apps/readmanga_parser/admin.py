from django.contrib import admin

from apps.readmanga_parser.models import (
    Translator,
    Author,
    Manga,
    Genre,
)


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'status', 'year',)
    list_filter = ('categories',)


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
