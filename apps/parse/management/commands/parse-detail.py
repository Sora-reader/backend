from django.core.management.base import CommandParser

from apps.core.abc.commands import BaseParseCommand
from apps.parse.models import Manga
from apps.parse.parsers import DETAIL_PARSER, PARSERS


class Command(BaseParseCommand):
    help = "Parse detailed information for manga"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("id", type=int, help="Id of the manga from the database")

    def handle(self, *args, **options):
        manga_id = options.get("id")

        try:
            manga: Manga = Manga.objects.get(pk=manga_id)
            self.logger.success("Manga found\n")
            parser = PARSERS[manga.source][DETAIL_PARSER]
            self.logger.success("Parser found\n")
            parser(manga.id)
            self.logger.info(f"Details for `{manga.title}` were parsed succesfully\n")
        except Manga.DoesNotExist:
            self.logger.error(f"Can't find manga with id {manga_id}\n")
        except KeyError:
            self.logger.error(f"Can't find details parser for {manga.source}")
        except Exception as exc:
            print(exc)
            self.logger.error("Some errors occured in the parser")
