from rest_framework import serializers

from apps.core.serializers import NameRelatedField
from apps.parse.models import Chapter, Manga


class MangaSerializer(serializers.ModelSerializer):
    authors = NameRelatedField(many=True)
    screenwriters = NameRelatedField(many=True)
    illustrators = NameRelatedField(many=True)
    translators = NameRelatedField(many=True)
    genres = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    categories = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = Manga
        fields = (
            "id",
            "source",
            "source_url",
            "title",
            "alt_title",
            "rating",
            "thumbnail",
            "image",
            "description",
            "authors",
            "screenwriters",
            "illustrators",
            "translators",
            "genres",
            "categories",
            "status",
            "year",
            "updated_chapters",
            "updated_detail",
        )


class MangaChaptersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"
