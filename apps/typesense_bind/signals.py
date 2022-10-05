from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.manga.models import Manga
from apps.manga.queries import fast_annotate_manga_query
from apps.typesense_bind.client import get_ts_client
from apps.typesense_bind.functions import upsert_collection

User = get_user_model()


@receiver(post_save, sender=Manga)
def update_collection(instance: Manga, **kwargs):
    client = get_ts_client()
    data = fast_annotate_manga_query(Manga.objects.filter(pk=instance.pk))
    upsert_collection(client, data)
