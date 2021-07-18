from django.apps import AppConfig
from django.core.checks import register

from apps.core.checks import check_redis


class CoreConfig(AppConfig):
    name = "apps.core"
    verbose_name = "Core"

    def ready(self) -> None:
        register(check_redis)
        return super().ready()
