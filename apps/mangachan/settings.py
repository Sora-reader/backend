import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "manga_reader.settings"  # noqa
django.setup()  # noqa

from apps.mangachan.pipelines import MangachanPipeline  # noqa
from apps.parse.scrapy.base_settings import *  # noqa

BOT_NAME = "mangachan"
SPIDER_MODULES = [
    "apps.mangachan.list",
    "apps.mangachan.detail",
    "apps.mangachan.chapter",
    "apps.mangachan.images",
]
# Remove for now as GAE workspace is immutable
LOG_FILE = "parse-mangachan.log"

DOWNLOADER_MIDDLEWARES = {
    "apps.parse.middleware.ErrorLoggerMiddleware": 340,
    "apps.parse.middleware.ProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 400,
}
ITEM_PIPELINES = {
    MangachanPipeline: 300,
}
