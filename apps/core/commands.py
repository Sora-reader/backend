from functools import partial

from django.core.management.base import BaseCommand


class ParseCommandLogger:
    def __init__(self, stdout, style) -> None:
        self.success = partial(stdout.write, style_func=style.SUCCESS)
        self.info = partial(stdout.write, style_func=style.NOTICE)
        self.error = partial(stdout.write, style_func=style.ERROR)


class BaseParseCommand(BaseCommand):
    logger: "ParseCommandLogger"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = ParseCommandLogger(self.stdout, self.style)
