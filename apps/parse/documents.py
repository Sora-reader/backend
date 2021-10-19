from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Manga


@registry.register_document
class MangaDocument(Document):
    class Index:
        name = "mangas"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Manga

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "title",
            "alt_title",
        ]
