from rest_framework import serializers

from apps.core.serializers import NameRelatedField
from apps.parse.models import Manga, Person


class MangaSerializer(serializers.ModelSerializer):
    authors = NameRelatedField(many=True)
    genres = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    categories = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    def get_authors(self, obj: Manga):
        return obj.authors.values_list(Person.NAME_FIELD).all()

    class Meta:
        model = Manga
        fields = (
            "id",
            "source",
            "title",
            "alt_title",
            "thumbnail",
            "image",
            "description",
            "authors",
            "genres",
            "categories",
            "status",
            "year",
        )


class MangaChaptersSerializer(serializers.Serializer):
    class Meta:
        fields = ("chapters",)
