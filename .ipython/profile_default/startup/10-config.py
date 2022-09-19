from django.contrib.postgres.aggregates import ArrayAgg  # noqa
from django.core.cache import cache  # noqa
from django.db import connection  # noqa
from django.db.models import *  # noqa
from django.db.models.functions import *  # noqa
from rich import inspect, pretty  # noqa

pretty.install()
