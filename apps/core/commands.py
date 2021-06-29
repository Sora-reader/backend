from functools import partial

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import termcolors


class BaseParseCommand(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        class Logger:
            def __init__(self_) -> None:
                self_.info = partial(
                    self.stdout.write,
                    style_func=termcolors.make_style(fg=settings.DJANGO_COLORS, opts=["bold"]),
                )
                self_.error = partial(
                    self.stdout.write,
                    style_func=self.style.ERROR,
                )

        self.__dict__.update({"logger_": Logger()})
