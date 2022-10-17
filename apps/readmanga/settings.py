import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "manga_reader.settings"  # noqa
django.setup()  # noqa

from apps.parse.base_settings import *  # noqa
from apps.readmanga.pipelines import ReadmangaPipeline  # noqa

BOT_NAME = "readmanga"
SPIDER_MODULES = [
    "apps.readmanga.list",
    "apps.readmanga.detail",
    "apps.readmanga.chapter",
    "apps.readmanga.images",
]
# Remove for now as GAE workspace is immutable
LOG_FILE = "parse-readmanga.log"

DOWNLOADER_MIDDLEWARES = {
    "apps.parse.middleware.ErrorLoggerMiddleware": 340,
    "apps.parse.middleware.ProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 400,
}
ITEM_PIPELINES = {
    ReadmangaPipeline: 300,
}
