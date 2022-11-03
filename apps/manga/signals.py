from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.manga.models import SaveList, SaveListNameChoices

LIST_NAMES = [n for n, _ in SaveListNameChoices.choices]


def create_save_lists(**kwargs):
    SaveList.objects.bulk_create(
        [SaveList(name=x, **kwargs) for x in LIST_NAMES], ignore_conflicts=True
    )


@receiver(post_save, sender=User)
def signal_handler(instance, **kwargs):
    create_save_lists(user=instance)
