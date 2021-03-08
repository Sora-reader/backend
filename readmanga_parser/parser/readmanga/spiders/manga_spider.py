from typing import Union
import scrapy
from scrapy import item
from ..readmanga_map import get_manga_urls
from scrapy.selector import Selector
from readmanga.items import Manga
from readmanga.spiders.consts import (
    TRANSLATORS_TAG,
    AUTHOR_TAG,
    NAME_TAG,
    YEAR_TAG,
    GENRES_TAG,
    DESCRIPTION_TAG
)


def get_first_or_empty(response, tag: str) -> str:
    try:
        return response.xpath(tag).extract()[0]
    except IndexError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = 'manga'

    def start_requests(self):
        urls = get_manga_urls()[:50]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        manga = Manga()
        manga['year'] = get_first_or_empty(response, YEAR_TAG)
        manga['author'] = get_first_or_empty(response, AUTHOR_TAG)
        # didnt handle that one due to only technical urls have no names
        manga['name'] = response.xpath(NAME_TAG).extract()[0]
        manga['genres'] = response.xpath(GENRES_TAG).extract()
        manga['translators'] = response.xpath(TRANSLATORS_TAG).extract()

        manga['description'] = get_first_or_empty(response, DESCRIPTION_TAG)

        return manga
