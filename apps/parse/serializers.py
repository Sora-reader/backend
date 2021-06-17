from rest_framework import serializers

from apps.parse.models import Manga


class MangaSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="name", read_only=True)
    genres = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    translators = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    categories = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    illustrators = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    screenwriters = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = Manga
        fields = "__all__"
