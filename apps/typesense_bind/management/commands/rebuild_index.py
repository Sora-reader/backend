import logging

from django.core.management.base import BaseCommand
from typesense.exceptions import ObjectNotFound

from apps.manga.models import Manga
from apps.typesense_bind.client import get_ts_client
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

        mangas = list(Manga.objects.values('id', 'title', 'alt_title'))
        # Yeah, I know
        mangas = [
            {'id': str(m['id']), 'title': m['title'], 'alt_title': m['alt_title']}
            for m in mangas
        ]

        res = client.collections[schema_name].documents.import_(mangas, {'action': 'upsert'})
        logger.info(f"Imported {len(res)} documents")
