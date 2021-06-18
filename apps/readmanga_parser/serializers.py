from rest_framework import serializers

from apps.readmanga_parser.models import Manga


class MangaSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="name", read_only=True)
    genres = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    categories = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = Manga
        fields = "__all__"


class MangaChaptersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ("chapters",)
