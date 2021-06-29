from django.core.management.base import CommandParser

from apps.core.commands import BaseParseCommand
from apps.parse import parsers
from apps.parse.models import Manga


class Command(BaseParseCommand):
    help = "Chapters parsing"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("id", type=int, help="Id of the manga from the database")

    def check_rss_url(self, manga: Manga):
        if not manga.rss_url:
            self.logger.error("Manga doesn't consists rss url. Parse the details")
            exit(0)

    def handle(self, *args, **options):
        manga_id = options.get("id")
        try:
            manga = Manga.objects.get(pk=manga_id)

            self.logger.info("Manga found\n")

            self.check_rss_url(manga)
            if manga.source == "Readmanga":
                self.logger.info("Parser found\n")
                parsers.readmanga_chapter_parse(manga.id, self.logger)
                self.logger.info(f"Manga `{manga.title}` parsed succesfully\n")
            else:
                self.logger.error("Parser not found\n")
        except Manga.DoesNotExist:
            self.logger.error(f"Can't find manga with id {manga_id}\n")
        except Exception as exc:
            self.logger.error(exc)
            self.logger.error("Some errors occured in the parser")
