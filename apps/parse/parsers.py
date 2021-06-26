import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apps.parse.readmanga.chapter_parser.parse import chapters_manga_info
from apps.parse.readmanga.detail_parser.parse import deepen_manga_info
from apps.parse.readmanga.list_parser.manga_spider import MangaSpider

SETTINGS_PATH = "apps.parse.readmanga.list_parser.settings"


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


def readmanga_chapter_parse(id):
    # TODO - add logging
    chapters_manga_info(id)
