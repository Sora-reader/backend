import logging
import sys

from django.core.management.base import BaseCommand, CommandParser

from apps.parse.exceptions import ParsingError
from apps.parse.parser import CHAPTER_PARSER, DETAIL_PARSER, IMAGE_PARSER, PARSER_TYPES
from apps.parse.source import CATALOGUE_NAMES
from apps.parse.tasks import run_spider_task

logger = logging.getLogger("management")


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "type",
            type=str,
            choices=PARSER_TYPES,
            help="which type of data to parse",
        )
        parser.add_argument(
            "catalogue",
            type=str,
            default="readmanga",
            choices=CATALOGUE_NAMES,
            help="parser to use which respresents a website source",
        )
        parser.add_argument(
            "--url",
            type=str,
            required=sys.argv[2] in [DETAIL_PARSER, CHAPTER_PARSER, IMAGE_PARSER],
            help="A link which to parse (detail/chapter/rss url)",
        )

    def handle(self, *args, **options):
        catalogue_name: str = options["catalogue"]
        try:
            logger.info("Running parser")
            run_spider_task(options["type"], catalogue_name, url=options["url"])
            logger.info("Finished parsing")
        except (AttributeError, KeyError):
            logger.error(f"Can't find Catalogue [{catalogue_name}]")
        except ParsingError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(f"Some errors occurred in the parser {catalogue_name} {e}")
