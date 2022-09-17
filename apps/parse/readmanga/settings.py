import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "manga_reader.settings"  # noqa
django.setup()  # noqa

from apps.parse.readmanga.pipelines import ReadmangaPipeline  # noqa
from apps.parse.scrapy.base_settings import *  # noqa

BOT_NAME = "readmanga"
SPIDER_MODULES = ["apps.parse.readmanga.list"]
LOG_FILE = "parse-readmanga.log"

DOWNLOADER_MIDDLEWARES = {
    "apps.parse.scrapy.middleware.ErrbackMiddleware": 340,
    "apps.parse.scrapy.middleware.ProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 400,
}
ITEM_PIPELINES = {
    ReadmangaPipeline: 300,
}
