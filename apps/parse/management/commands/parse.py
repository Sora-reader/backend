import logging

from django.core.management.base import CommandParser

from apps.core.commands import BaseParseCommand
from apps.parse import parsers

SETTINGS_PATH = "apps.parse.readmanga.list_parser.settings"


class Command(BaseParseCommand):
    help = "Parse manga list"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "parser",
            type=str,
            default="readmanga",
            choices=["readmanga"],
            help="parser to use which respresents a website source",
        )

    def handle(self, *args, **options):
        parser_name = options.get("parser")
        try:
            parser = getattr(parsers, f"{parser_name}_parser")

            self.logger.success("Parser found\n")

            # Mute all output
            logging.getLogger("urllib3").setLevel(logging.CRITICAL)
            logging.getLogger("requests").setLevel(logging.CRITICAL)
            logging.getLogger("scrapy").setLevel(logging.CRITICAL)
            logging.getLogger("scrapy.spiders").setLevel(logging.CRITICAL)
            logging.getLogger("scrapy").propagate = False
            logging.getLogger("scrapy.spiders").propagate = False

            # Clear log file
            try:
                open("parse-readmanga.log", "w")
            except Exception:
                pass

            parser(
                logger=self.logger,
                settings={
                    # Log stdout and errors to file
                    "LOG_FILE": "parse-readmanga.log",
                    "LOG_STDOUT": True,
                },
            )
            self.logger.success("\nFinished parsing")
        except AttributeError:
            self.logger.error(f"Can't find parser [{parser_name}]")
        except Exception:
            self.logger.error(f"Some errors occured in the parser {parser_name}")
