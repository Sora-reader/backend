from django.apps import AppConfig


class Config(AppConfig):
    name = "apps.mangachan"

    def ready(self):
        from . import Mangachan  # noqa
        from .detail import MangachanDetailSpider  # noqa
        from .image import MangachanImageSpider  # noqa
        from .list import MangachanListSpider  # noqa
