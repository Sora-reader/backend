import os

from celery import Celery

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
app.autodiscover_tasks()
