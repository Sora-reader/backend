import logging
import sys

from django.core.management.base import BaseCommand, CommandParser

from apps.parse.const import (
    CATALOGUE_NAMES,
    CHAPTER_PARSER,
    DETAIL_PARSER,
    IMAGE_PARSER,
    PARSER_TYPES,
)
from apps.parse.scrapy.utils import run_parser
from apps.parse.utils import mute_logger_stdout

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
            "--pk",
            type=int,
            required=sys.argv[2] in [DETAIL_PARSER, CHAPTER_PARSER, IMAGE_PARSER],
            help="PK of an object to parse for",
        )

    def handle(self, *args, **options):
        mute_logger_stdout("scrapy", "elasticsearch", "asyncio", "protego", "urllib3", "requests")
        try:
            catalogue_name: str = options["catalogue"]
            logger.info("Running parser")
            run_parser(options["type"], catalogue_name, pk=options["pk"])
            logger.info("\nFinished parsing")
        except (AttributeError, KeyError):
            logger.error(f"Can't find Catalogue [{catalogue_name}]")
        except Exception:
            logger.error(f"Some errors occured in the parser {catalogue_name}")
