from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.db.models.query import QuerySet

from apps.core.abc.admin import BaseAdmin, BaseTabularInline, ImagePreviewMixin, RelatedField
from apps.manga.models import Author, Category, Chapter, Genre, Manga, Person, PersonRelatedToManga
from apps.parse.catalogue import Catalogue


class ChapterInline(BaseTabularInline):
    model = Chapter
    fields = ("title", "chapter_link")
    verbose_name = "Chapter"
    verbose_name_plural = "Chapters"
    readonly_fields = ("chapter_link",)

    @staticmethod
    def chapter_link(obj):
        return obj.chapter.link


class PersonInline(BaseTabularInline):
    model = PersonRelatedToManga
    verbose_name = "Person"
    verbose_name_plural = "Persons"


class SourceFilter(SimpleListFilter):
    title = "source"
    parameter_name = "source"

    def lookups(self, request, model_admin):
        return zip(Catalogue.map.sources, Catalogue.map.names)

    def queryset(self, request, queryset: QuerySet):
        value = self.value()
        if value:
            return queryset.filter(source_url__startswith=value)
        return queryset


@admin.register(Manga)
class MangaAdmin(BaseAdmin, ImagePreviewMixin, admin.ModelAdmin):
    search_fields = ("title",)
    inlines = (
        ChapterInline,
        PersonInline,
    )
    list_display = (
        "custom_title",
        "source",
        "get_image",
        "authors",
        "rating",
        "status",
        "genre_list",
    )
    readonly_fields = ("identifier", "source_url", "chapters_url")
    list_filter = (
        "genres",
        SourceFilter,
    )

    def custom_title(self, obj: Manga):
        concat = f"{obj.title}{', ' + obj.year if obj.year else ''}"
        if len(concat) > 30:
            return concat[:30] + "..."
        return concat

    custom_title.short_description = "Title"  # noqa

    authors = RelatedField(Manga.authors, description="Authors", html=True)
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


@admin.register(Category)
class CategoryAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Chapter)
class ChapterAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title", "manga_name")
    list_filter = ("manga",)
    filter_input_length = {
        "manga": 5,
    }

    @staticmethod
    def manga_name(obj):
        return obj.manga.title
