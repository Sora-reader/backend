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
            "number", type=int, help="Chapter of the manga's volume from the database"
        )

    def handle(self, id, vol, number, *args, **kwargs):
        try:
            chapter: Chapter = Chapter.objects.get(number=number, volume=vol, manga__id=id)
            self.logger.success("Chapter found\n")
            manga: Manga = chapter.manga_set.first()
            if manga.source == "Readmanga":
                self.logger.success("Parser found\n")
                parsers.readmanga_image_parse(chapter)
                self.logger.info(
                    f"Chapter `{vol}/{number}` images for `{manga.title}` were parsed succesfully\n"
                )
            else:
                self.logger.error("Parser not found\n")
        except Manga.DoesNotExist:
            self.logger.error(f"Can't find manga with id {id}\n")
        except Chapter.DoesNotExist:
            self.logger.error(
                "Can't find chapter with provided vol and chapter. Try to parse chapters\n"
            )
        except Exception as exc:
            print(exc)
            self.logger.error("Some errors occured in the parser")
