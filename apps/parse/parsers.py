import asyncio
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apps.parse.mangalib.detail_parser.parser import detail_manga_parser
from apps.parse.mangalib.list_parser.parser import Crawler
from apps.parse.models import Manga
from apps.parse.readmanga.chapter_parser.parse import chapters_manga_info
from apps.parse.readmanga.detail_parser.parse import deepen_manga_info
from apps.parse.readmanga.images_parser.parse import images_manga_info
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

    process.crawl(MangaSpider, logger=logger)
    process.start()


def mangalib_parser(settings=None, logger=None):
    crawler = Crawler(logger=logger)
    asyncio.get_event_loop().run_until_complete(crawler.get_list())


DETAIL_PARSER = "details"
LIST_PARSER = "list"
IMAGE_PARSER = "images"
CHAPTER_PARSER = "chapters"

PARSERS = {
    Manga.SOURCE_MAP.get("https://readmanga.live"): {
        DETAIL_PARSER: deepen_manga_info,
        CHAPTER_PARSER: chapters_manga_info,
        IMAGE_PARSER: images_manga_info,
        LIST_PARSER: readmanga_parser,
    },
    Manga.SOURCE_MAP.get("https://mangalib.me"): {
        DETAIL_PARSER: detail_manga_parser,
        LIST_PARSER: mangalib_parser,
    },
}
