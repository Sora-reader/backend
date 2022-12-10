from django.core.management.base import BaseCommand

from apps.manga.models import Manga
from apps.parse.tasks import run_spider_task
from apps.parse.types import ParserType


class Command(BaseCommand):
    def handle(self, *args, **options):
        top_10 = Manga.objects.filter(popularity=2)

        for manga in top_10:
            run_spider_task(ParserType.detail, "readmanga", url=manga.source_url)
            run_spider_task(ParserType.chapter, "readmanga", url=manga.chapters_url)
            for num, chapter in enumerate(manga.chapters.all(), 1):
                print(f"chapter images #{num}/{len(manga.chapters.all())}")
                run_spider_task(ParserType.image, "readmanga", url=chapter.link)
