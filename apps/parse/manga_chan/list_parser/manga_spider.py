import re

import requests
import scrapy
from lxml import etree
from scrapy.http import HtmlResponse
from twisted.python.failure import Failure

from apps.core.commands import ParseCommandLogger

from .consts import (
    ALT_TITLE_TAG,
    FULL_TITLE_TAG,
    GENRES_TAG,
    IMAGE_TAG,
    MANGA_CARD_TAG,
    PAGE_SELECTOR,
    SOURCE_URL_TAG,
)

MANGA_CHAN_URL = "https://manga-chan.me"


class MangaChanSpider(scrapy.Spider):
    management_logger: "ParseCommandLogger"
    name = "manga_chan"

    def __init__(self, *args, logger, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update({"management_logger": logger})

    @property
    def logger(self):
        return self.management_logger

    def start_requests(self):
        self.logger.info("Starting requests")
        self.logger.info("=================")
        mangas_list = requests.get(f"{MANGA_CHAN_URL}/catalog")
        if not mangas_list.status_code == 200:
            self.logger.error(f"Failed request with code {mangas_list.status_code}")
            return
        mangas_list = mangas_list.text
        html_parser = etree.HTML(mangas_list)
        standard_offset = 20
        max_page = html_parser.xpath(PAGE_SELECTOR)[-1]
        max_offset = (int(max_page) - 1) * standard_offset
        base_url = f"{MANGA_CHAN_URL}/catalog?offset="
        offsets = [offset for offset in range(0, max_offset, standard_offset)]
        urls = [base_url + str(offset) for offset in offsets]

        for url, offset in zip(urls, offsets):
            yield scrapy.Request(url=url, callback=self.parse, meta={"offset": offset})

    def request_fallback(self, failure: Failure):
        self.logger.error(
            f'Request for url "{failure.value.response.url}" '
            f"failed with status {failure.value.response.status}"
        )

    def parse(self, response):
        mangas = []
        manga_cards = response.xpath(MANGA_CARD_TAG).extract()
        offset = response.meta["offset"]
        for index, manga_card in enumerate(manga_cards):
            response = HtmlResponse(url="", body=manga_card, encoding="utf-8")
            full_title = response.xpath(FULL_TITLE_TAG).extract_first("")
            source_url = MANGA_CHAN_URL + response.xpath(SOURCE_URL_TAG).extract_first("")
            genres = response.xpath(GENRES_TAG).extract()
            image = response.xpath(IMAGE_TAG).extract_first("")
            alt_title = response.xpath(ALT_TITLE_TAG).extract_first("")
            popularity = offset + index + 1
            title = (
                re.search(r" \((.+?)\)", full_title).group(1)
                if re.search(r" \((.+?)\)", full_title)
                else alt_title
            )

            mangas.append(
                {
                    "popularity": popularity,
                    "title": title,
                    "alt_title": alt_title,
                    "source_url": source_url,
                    "genres": genres,
                    "image": image,
                    "thumbnail": image,
                }
            )
            self.logger.info('Parsed manga "{}"'.format(title))

        self.logger.info("Processing items...")
        self.logger.info("===================")
        return mangas
