import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apps.parse.readmanga.chapter_parser.parse import chapters_manga_info
from apps.parse.readmanga.detail_parser.parse import deepen_manga_info
from apps.parse.readmanga.images_parser.parse import images_manga_info
from apps.parse.readmanga.list_parser import READMANGA_SETTINGS_PATH
from apps.parse.readmanga.list_parser.manga_spider import MangaSpider


def readmanga_parser(settings=None, logger=None):
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", READMANGA_SETTINGS_PATH)
    process = CrawlerProcess(
        {
            **get_project_settings(),
            **(settings if settings else {}),
        }
    )

    process.crawl(MangaSpider, logger=logger)
    process.start()


DETAIL_PARSER = "details"
LIST_PARSER = "list"
IMAGE_PARSER = "images"
CHAPTER_PARSER = "chapters"


PARSERS = {
    "https://readmanga.io": {
        DETAIL_PARSER: deepen_manga_info,
        CHAPTER_PARSER: chapters_manga_info,
        IMAGE_PARSER: images_manga_info,
        LIST_PARSER: readmanga_parser,
    },
}
