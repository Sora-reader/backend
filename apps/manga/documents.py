from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from apps.manga.models import Manga


@registry.register_document
class MangaDocument(Document):
    class Index:
        name = "mangas"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Manga

        fields = [
            "title",
            "alt_title",
        ]
