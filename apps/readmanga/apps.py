from django.apps import AppConfig


class Config(AppConfig):
    name = "apps.readmanga"

    def ready(self):
        from . import Readmanga  # noqa
        from .chapter import ReadmangaChapterSpider  # noqa
        from .detail import ReadmangaDetailSpider  # noqa
        from .image import ReadmangaImageSpider  # noqa
        from .list import ReadmangaListSpider  # noqa
