import time
import scrapy
import logging
from readmanga_parser.parser.readmanga.readmanga_map import get_manga_urls
from readmanga_parser.parser.readmanga.items import MangaItem
from readmanga_parser.parser.readmanga.spiders.consts import (
    AUTHOR_TAG,
    DESCRIPTION_TAG,
    GENRES_TAG,
    NAME_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)
logging.basicConfig(level=logging.ERROR)


def get_first_or_empty(response, tag: str) -> str:
    try:
        return response.xpath(tag).extract()[0]
    except IndexError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "manga"

    def start_requests(self):
        urls = get_manga_urls()[:50]

        for url in urls:
            time.sleep(0.5)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        manga = MangaItem()
        manga['year'] = get_first_or_empty(response, YEAR_TAG)
        manga['author'] = get_first_or_empty(response, AUTHOR_TAG)
        # special handeling. Mangas without dont exist, so itll be technical page
        try:
            manga['name'] = response.xpath(NAME_TAG).extract()[0]
        except IndexError:
            logging.error("No manga name, likely it was technical URL")

        manga['genres'] = response.xpath(GENRES_TAG).extract()
        manga['translators'] = response.xpath(TRANSLATORS_TAG).extract()

        manga["description"] = get_first_or_empty(response, DESCRIPTION_TAG)

        return manga
