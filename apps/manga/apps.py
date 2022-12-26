from django.apps import AppConfig


class MangaConfig(AppConfig):
    name = "apps.manga"

    def ready(self):
        from . import signals  # noqa
