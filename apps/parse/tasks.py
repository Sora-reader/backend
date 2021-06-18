import os
import time
from contextlib import contextmanager

from celery import Task, current_app
from django.core.cache import cache
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apps.parse.models import TaskControl
from apps.parse.readmanga.readmanga.spiders.manga_spider import MangaSpider

SETTINGS_PATH = "apps.parse.readmanga.readmanga.settings"

app = current_app._get_current_object()

# Ten minutes
LOCK_EXPIRE = 60 * 10


@contextmanager
def lock_task_by_name(task_name: str):
    """Task locking function. The function intended
    for preventing other functions with the same name
    from executing by Celery.

    task_name - is a sometask.name where sometask is a Celery task

    In short, it uses key-value storage provided by Django. Keys have
    expiration time specified in LOCK_EXPIRE in seconds.

    """
    timeout_at = time.monotonic() + LOCK_EXPIRE
    status = cache.add(task_name, "lock", LOCK_EXPIRE)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(task_name)


@app.task(bind=True, name="parse_readmanga")
def parse_readmanga_task(self: Task):
    task_status = TaskControl.objects.filter(task_name=self.name, task_status=True)
    with lock_task_by_name(self.name) as lock:
        if lock and task_status:
            os.environ.setdefault("SCRAPY_SETTINGS_MODULE", SETTINGS_PATH)
            process = CrawlerProcess(get_project_settings())

            process.crawl(MangaSpider)
            process.start()
