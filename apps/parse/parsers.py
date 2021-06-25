import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apps.parse.readmanga.lxml_parser.detail_parse import deepen_manga_info
from apps.parse.readmanga.readmanga.spiders.manga_spider import MangaSpider

SETTINGS_PATH = "apps.parse.readmanga.readmanga.settings"


def readmanga_parser(settings=None, logger=None):
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", SETTINGS_PATH)
    process = CrawlerProcess(
        {
            **get_project_settings(),
            **(settings if settings else {}),
        }
    )

    process.crawl(MangaSpider, custom_logger=logger)
    process.start()


def readmanga_detail_parse(id):
    # TODO - add logging
    deepen_manga_info(id)
