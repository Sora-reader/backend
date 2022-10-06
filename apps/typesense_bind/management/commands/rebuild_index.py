import logging

from django.core.management.base import BaseCommand
from typesense.exceptions import ObjectNotFound

from apps.manga.annotate import fast_annotate_manga_query
from apps.manga.models import Manga
from apps.typesense_bind.client import get_ts_client
from apps.typesense_bind.functions import upsert_collection
from apps.typesense_bind.schema import schema, schema_name

logger = logging.getLogger("management")


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = get_ts_client()

        try:
            client.collections[schema_name].delete()
        except ObjectNotFound:
            pass

        client.collections.create(schema)
        logger.info("Recreated collection")

        mangas = fast_annotate_manga_query(Manga.objects.all())

        res = upsert_collection(client, mangas)
        logger.info(f"Imported {len(res)} documents")
