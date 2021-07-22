from django.core.management.base import CommandParser

from apps.core.commands import BaseParseCommand
from apps.parse import parsers
from apps.parse.models import Manga


class Command(BaseParseCommand):
    help = "Parse chapters for manga"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("id", type=int, help="Id of the manga from the database")

    def check_rss_url(self, manga: Manga):
        if not manga.rss_url:
            self.logger.error("Manga rss_url is not set. Parse the details first")
            exit(0)

    def handle(self, *args, **options):
        manga_id = options.get("id")
        try:
            manga = Manga.objects.get(pk=manga_id)
            print(manga.title, manga.source)
            self.logger.success("Manga found\n")

            if manga.source == "Readmanga":
                self.check_rss_url(manga)
                self.logger.success("Parser found\n")
                parsers.readmanga_chapter_parse(manga.id)
                self.logger.info(f"Chapters for `{manga.title}` were parsed succesfully\n")
            elif manga.source == "Mangalib":
                self.logger.success("Parser found\n")
                parsers.mangalib_chapter_parse(manga.id)
                self.logger.info(f"Chapters for `{manga.title}` were parsed succesfully\n")
            else:
                self.logger.error("Parser not found\n")
        except Manga.DoesNotExist:
            self.logger.error(f"Can't find manga with id {manga_id}\n")
        except Exception as exc:
            self.logger.error(exc)
            self.logger.error("Some errors occured in the parser")
