from django.apps import AppConfig


class TypesenseBindConfig(AppConfig):
    name = "apps.typesense_bind"

    def ready(self):
        from . import signals  # noqa
