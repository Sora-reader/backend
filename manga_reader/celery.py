import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_reader.settings")

app = Celery(
    "manga",
    broker="redis://user@redis//",
    backend="redis://",
)
app.config_from_object("manga_reader.celery_config", namespace="CELERY")
app.conf.update(
    result_expires=60 * 60,
)

app.conf.worker_max_tasks_per_child = 1
app.conf.beat_schedule.update(
    {
        "parsing": {
            "task": "apps.readmanga_parser.tasks.parse_readmanga_task",
            # schedule parsing at 1.01AM on a daily basis
            "schedule": crontab(hour=1, minute=1),
        },
    }
)
app.conf.timezone = "UTC"

app.autodiscover_tasks()
