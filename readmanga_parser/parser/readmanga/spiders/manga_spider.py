import logging
import re
import time

import scrapy

from readmanga_parser.parser.readmanga.descr_utils import clear_list_description, is_valid_description
from readmanga_parser.parser.readmanga.items import MangaItem
from readmanga_parser.parser.readmanga.readmanga_map import get_manga_urls
from readmanga_parser.parser.readmanga.spiders.consts import (
    AUTHOR_TAG,
    CHAPTERS_TAG,
    DESCRIPTION_ALT_TAG,
    DESCRIPTION_TAG,
    GENRES_TAG,
    IMAGE_TAG,
    NAME_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)

logging.getLogger(__name__)


def extract_description(response) -> str:
    desc = handle_xpath_response(response, DESCRIPTION_TAG)
    desc = clear_list_description(desc)
    if is_valid_description(desc):
        return desc
    else:
        desc = handle_xpath_response(response, DESCRIPTION_ALT_TAG)
        return desc


def handle_xpath_response(response, tag: str) -> str:
    try:
        return response.xpath(tag).extract()
    except IndexError:
        return ""


def chapters_into_dict(chapters: list) -> dict:
    regex = "[\n]+|[ ]{2,}"
    chapters = [re.sub(regex, "", chapter) for chapter in chapters]
    readmanga_base_url = "https://readmanga.live"
    links = filter(lambda m: m.startswith("/"), chapters)
    names = filter(lambda n: not n.startswith("/"), chapters)

    chapters_catalogue = {}
    for link, name in zip(links, names):
        chapters_catalogue.update({readmanga_base_url + link: name})

    return chapters_catalogue


class QuotesSpider(scrapy.Spider):
    name = "manga"

    def start_requests(self):
        urls = get_manga_urls()

        for url in urls:
            time.sleep(1)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        manga = MangaItem()
        manga["year"] = handle_xpath_response(response, YEAR_TAG)
        manga["author"] = handle_xpath_response(response, AUTHOR_TAG)
        # special handeling. Mangas without dont exist, so itll be technical page
        try:
            manga["name"] = response.xpath(NAME_TAG).extract()[0]
            manga["image"] = handle_xpath_response(response, IMAGE_TAG)[0]
        except IndexError:
            logging.error("No manga name or image, likely it was technical URL")

        manga["genres"] = response.xpath(GENRES_TAG).extract()
        manga["translators"] = response.xpath(TRANSLATORS_TAG).extract()

        manga["description"] = extract_description(response)

        chapters = handle_xpath_response(response, CHAPTERS_TAG)
        manga["chapters"] = chapters_into_dict(chapters)
        return manga
