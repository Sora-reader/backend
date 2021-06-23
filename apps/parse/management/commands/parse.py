import logging
from functools import partial

from django.core.management.base import BaseCommand, CommandParser
from django.utils import termcolors

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
            parser = getattr(parsers, f"{parser_name}_parser")

            self.stdout.write("Parser found\n", self.style.SUCCESS)

            # TODO: prettify and redirect loggers
            class Logger:
                def __init__(self_) -> None:
                    self_.info = partial(
                        self.stdout.write,
                        style_func=termcolors.make_style(fg="cyan", opts=["bold"]),
                    )
                    self_.error = partial(self.stdout.write, style_func=self.style.ERROR)

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
                logger=Logger(),
                settings={
                    # Log stdout and errors to file
                    "LOG_FILE": "parse-readmanga.log",
                    "LOG_STDOUT": True,
                },
            )
            self.stdout.write("\nFinished parsing", self.style.SUCCESS)
        except AttributeError:
            self.stdout.write(f"Can't find parser [{parser_name}]", self.style.ERROR)
        except Exception:
            self.stdout.write(f"Some errors occured in the parser {parser_name}", self.style.ERROR)
