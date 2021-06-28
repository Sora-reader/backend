from django.core.management.base import BaseCommand, CommandParser

from apps.parse import parsers
from apps.parse.models import Manga


class Command(BaseCommand):
    help = "Detailed parsing"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("id", type=int, help="Id of the manga from the database")

    def handle(self, *args, **options):
        manga_id = options.get("id")
        try:
            manga = Manga.objects.get(pk=manga_id)

            self.stdout.write("Manga found\n", self.style.SUCCESS)

            if manga.source == Manga.SOURCE_MAP["readmanga.live"]:
                self.stdout.write("Parser found\n", self.style.SUCCESS)
                parsers.readmanga_detail_parse(manga.id)
                self.stdout.write(f"Manga `{manga.title}` parsed succesfully\n", self.style.SUCCESS)
            else:
                self.stdout.write("Parser not found\n", self.style.ERROR)
        except Manga.DoesNotExist:
            self.stdout.write(f"Can't find manga with id {manga_id}\n", self.style.ERROR)
        except Exception as exc:
            print(exc)
            self.stdout.write("Some errors occured in the parser", self.style.ERROR)
