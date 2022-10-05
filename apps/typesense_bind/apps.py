from django.apps import AppConfig


class TypesenseBindConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.typesense_bind"

    def ready(self):
        from . import signals  # noqa
