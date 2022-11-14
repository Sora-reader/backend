import sys

from django.core.management.base import BaseCommand, CommandParser

from apps.parse.catalogue import Catalogue
from apps.parse.exceptions import NotFound, ParsingError
from apps.parse.tasks import run_spider_task
from apps.parse.types import ParserType


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "type",
            type=str,
            choices=list(ParserType),
            help="which type of data to parse",
        )
        parser.add_argument(
            "catalogue",
            type=str,
            default="readmanga",
            choices=Catalogue.map.names,
            help="parser to use which represents a website source",
        )
        parser.add_argument(
            "--url",
            type=str,
            required=sys.argv[2] in list(ParserType),
            help="A link which to parse (detail/chapter/rss url)",
        )

    def handle(self, *args, **options):
        catalogue_name: str = options["catalogue"]
        try:
            self.stdout.write("Running parser")
            run_spider_task(options["type"], catalogue_name, url=options["url"])
            self.stdout.write("Finished parsing")
        except NotFound as e:
            self.stderr.write(f"Can't find {e}")
        except ParsingError as e:
            self.stderr.write(str(e))
        except Exception as e:
            self.stderr.write(f"Some errors occurred in the parser {catalogue_name} {e}")
            raise e
