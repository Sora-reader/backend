
from django.core.management.base import BaseCommand
from typesense.exceptions import ObjectNotFound

from apps.manga.annotate import fast_annotate_manga_query
from apps.manga.models import Manga
from apps.typesense_bind.client import get_ts_client
from apps.typesense_bind.functions import upsert_collection
from apps.typesense_bind.schema import schema, schema_name


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = get_ts_client()

        try:
            client.collections[schema_name].delete()
        except ObjectNotFound:
            pass

        client.collections.create(schema)
        self.stdout.write("Recreated collection")

        mangas = fast_annotate_manga_query(Manga.objects.all())

        start = 0
        step = 1000
        end = len(mangas)
        inserted = 0
        self.stdout.write(f"Importing {end} documents")
        for chunk_start in range(start, end, step):
            inserted += len(upsert_collection(client, mangas[chunk_start:chunk_start + step]))
            self.stdout.write(f'=> imported {inserted} documents')

        self.stdout.write(f"finished importing {inserted} documents")
