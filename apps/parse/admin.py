from django.contrib import admin

from apps.core.admin import BaseAdmin, BaseTabularInline, ImagePreviewMixin, RelatedField
from apps.parse.models import Author, Chapter, Genre, Manga, Person, PersonRelatedToManga


@admin.display(description="Manga")
def manga_name(obj):
    return obj.manga_set.first().title


class ChapterInline(BaseTabularInline):
    model = Manga.chapters.through
    fields = ("chapter", "chapter_link")
    verbose_name = "Chapter"
    verbose_name_plural = "Chapters"
    readonly_fields = ("chapter_link",)

    def chapter_link(self, obj):
        return obj.chapter.link


class PersonInline(BaseTabularInline):
    model = PersonRelatedToManga
    verbose_name = "Person"
    verbose_name_plural = "Persons"


@admin.register(Manga)
class MangaAdmin(BaseAdmin, ImagePreviewMixin, admin.ModelAdmin):
    search_fields = ("title", "alt_title")
    inlines = [
        ChapterInline,
        PersonInline,
    ]
    list_display = (
        "custom_title",
        "get_image",
        "authors",
        "rating",
        "status",
        "genre_list",
    )

    def custom_title(self, obj: Manga):
        concat = f"{obj.title}{', ' + obj.year if obj.year else ''}"
        if len(concat) < 30:
            concat += f" ({obj.alt_title})"
        return concat

    custom_title.short_description = "Title"

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


@admin.register(Chapter)
class ChapterAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title", manga_name)
    list_filter = ("manga",)
