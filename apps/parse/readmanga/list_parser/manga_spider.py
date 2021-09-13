import logging

import requests
import scrapy
from django.conf import settings
from lxml import etree
from scrapy.http import HtmlResponse
from twisted.python.failure import Failure

from apps.core.abc.commands import ParseCommandLogger
from apps.parse.readmanga.list_parser.utils import parse_rating

from .consts import (
    ALT_TITLE_URL,
    GENRES_TAG,
    MANGA_TILE_TAG,
    SOURCE_URL_TAG,
    STAR_RATE_TAG,
    THUMBNAIL_IMG_URL_TAG,
    TITLE_TAG,
)

logging.getLogger(__name__)
READMANGA_URL = "https://readmanga.live"


class MangaSpider(scrapy.Spider):
    management_logger: "ParseCommandLogger"
    name = "manga"

    def __init__(self, *args, logger, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update({"management_logger": logger})

    @property
    def logger(self):
        return self.management_logger

    def start_requests(self):
        self.logger.info("Starting requests")
        self.logger.info("=================")
        mangas_list = requests.get(f"{READMANGA_URL}/list", headers=settings.HEADERS)
        if not mangas_list.status_code == 200:
            self.logger.error(f"Failed request with code {mangas_list.status_code}")
            return
        mangas_list = mangas_list.text

        xpath_selector = '//a[@class = "step"]/text()'
        html_parser = etree.HTML(mangas_list)
        maximum_page = html_parser.xpath(xpath_selector)[-1]
        standart_offset = 70
        maximum_offset = (int(maximum_page) - 1) * standart_offset

        base_url = f"{READMANGA_URL}/list?&offset="
        offsets = [offset for offset in range(0, maximum_offset, standart_offset)]
        urls = [base_url + str(offset) for offset in offsets]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def request_fallback(self, failure: Failure):
        self.logger.error(
            f'Request for url "{failure.value.response.url}" '
            f"failed with status {failure.value.response.status}"
        )

    def parse(self, response):
        mangas = []
        descriptions = response.xpath(MANGA_TILE_TAG).extract()
        for description in descriptions:
            response = HtmlResponse(url="", body=description, encoding="utf-8")

            rating = parse_rating(response.xpath(STAR_RATE_TAG).extract_first(""))
            title = response.xpath(TITLE_TAG).extract_first("")
            source_url = response.xpath(SOURCE_URL_TAG).extract_first("")
            genres = response.xpath(GENRES_TAG).extract()
            thumbnail = response.xpath(THUMBNAIL_IMG_URL_TAG).extract_first("")
            image = thumbnail.replace("_p", "")
            alt_title = response.xpath(ALT_TITLE_URL).extract_first("")

            mangas.append(
                {
                    "rating": rating,
                    "title": title,
                    "alt_title": alt_title,
                    "thumbnail": thumbnail,
                    "image": image,
                    "genres": genres,
                    "source_url": READMANGA_URL + source_url,
                }
            )
            self.logger.info('Parsed manga "{}"'.format(title))

        self.logger.info("Processing items...")
        self.logger.info("===================")
        return mangas
