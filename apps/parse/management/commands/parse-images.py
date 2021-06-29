from django.core.management.base import CommandParser

from apps.core.commands import BaseParseCommand
from apps.parse import parsers
from apps.parse.models import Chapter, Manga


class Command(BaseParseCommand):
    help = "Parser of the manga's images"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("id", type=int, help="Id of the manga from the database")
        parser.add_argument("vol", type=int, help="Volume of the manga from the database")
        parser.add_argument(
            "chapter", type=int, nargs="?", help="Chapter of the manga's volume from the database"
        )

    def handle(self, *args, **options):
        manga_id = options.get("id")

        try:
            manga: Manga = Manga.objects.get(pk=manga_id)
            self.logger.success("Manga found\n")

            if manga.source == "Readmanga":
                self.logger.success("Parser found\n")
                chapter: Chapter = manga.volumes.get(
                    volume=options.get("vol"), number=options.get("chapter")
                )
                print(parsers.readmanga_image_parse(chapter.link))
                self.logger.success(f"Manga `{manga.title}` parsed succesfully\n")
            else:
                self.logger.error("Parser not found\n")
        except Manga.DoesNotExist:
            self.logger.error(f"Can't find manga with id {manga_id}\n")
        except Chapter.DoesNotExist:
            self.logger.error(
                "Can't find chapter with provided vol and chapter. Try to parse chapters\n"
            )
        except Exception as exc:
            print(exc)
            self.logger.error("Some errors occured in the parser")
