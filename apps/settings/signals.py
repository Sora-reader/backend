from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.settings.models import UserPreferences


@receiver(post_save, sender=User)
def create_prefs_handler(instance, **kwargs):  # noqa
    UserPreferences.objects.create(user=instance)
