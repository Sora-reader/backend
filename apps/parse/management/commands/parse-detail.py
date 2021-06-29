from django.core.management.base import CommandParser

from apps.core.commands import BaseParseCommand
from apps.parse import parsers
from apps.parse.models import Manga


class Command(BaseParseCommand):
    help = "Detailed parsing"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("id", type=int, help="Id of the manga from the database")

    def handle(self, *args, **options):
        manga_id = options.get("id")

        try:
            manga = Manga.objects.get(pk=manga_id)
            self.logger_.info("Manga found\n")

            if manga.source == Manga.SOURCE_MAP["readmanga.live"]:
                self.logger_.info("Parser found\n")
                parsers.readmanga_detail_parse(manga.id)
                self.logger_.info(f"Manga `{manga.title}` parsed succesfully\n")
            else:
                self.logger_.error("Parser not found\n")
        except Manga.DoesNotExist:
            self.logger_.error(f"Can't find manga with id {manga_id}\n")
        except Exception as exc:
            print(exc)
            self.logger_.error("Some errors occured in the parser")
