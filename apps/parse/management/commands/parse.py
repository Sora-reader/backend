from django.core.management.base import BaseCommand, CommandParser

from apps.parse import parsers

SETTINGS_PATH = "apps.parse.readmanga.readmanga.settings"


class Command(BaseCommand):
    help = """Execute different parser of mangas

    `python3 manage.py parse [readmanga | otherparser]`
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "parser",
            nargs="?",
            type=str,
        )

    def handle(self, *args, **options):
        parser_name = options.get("parser")
        try:
            getattr(parsers, f"{parser_name}_parser")()
        except AttributeError:
            self.stdout.write(f"Can't find parser [{parser_name}]", self.style.ERROR)
        except Exception:
            self.stdout.write(f"Some errors occured in the parser {parser_name}", self.style.ERROR)
