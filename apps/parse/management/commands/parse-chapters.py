from django.core.management.base import CommandParser

from apps.core.commands import BaseParseCommand
from apps.parse.models import Manga
from apps.parse.parsers import CHAPTER_PARSER, PARSERS


class Command(BaseParseCommand):
    help = "Parse chapters for manga"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("id", type=int, help="Id of the manga from the database")

    def check_rss_url(self, manga: Manga):
        if manga.source == "Readmanga" and not manga.rss_url:
            self.logger.error("Manga rss_url is not set. Parse the details first")
            exit(0)

    def handle(self, *args, **options):
        manga_id = options.get("id")
        try:
            manga = Manga.objects.get(pk=manga_id)
            print(manga.title, manga.source)
            self.logger.success("Manga found\n")

            self.check_rss_url(manga)
            parser = PARSERS[manga.source][CHAPTER_PARSER]
            self.logger.success("Parser found\n")
            parser(manga.id)
            self.logger.info(f"Chapters for `{manga.title}` were parsed succesfully\n")
        except Manga.DoesNotExist:
            self.logger.error(f"Can't find manga with id {manga_id}\n")
        except KeyError:
            self.logger.error("Can't find chapters parser\n")
        except Exception as exc:
            self.logger.error(exc)
            self.logger.error("Some errors occured in the parser")
