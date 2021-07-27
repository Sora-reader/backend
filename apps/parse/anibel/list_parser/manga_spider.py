import logging

import requests
import scrapy
from lxml import etree
from scrapy.http import HtmlResponse
from twisted.python.failure import Failure

from apps.core.commands import ParseCommandLogger

from .consts import GENRES_TAG, MANGA_CARD_TAG, SOURCE_URL_TAG, THUMBNAIL_IMG_URL_TAG, TITLE_TAG

logging.getLogger(__name__)
ANIBEL_URL = "https://anibel.net"


class AnibelMangaSpider(scrapy.Spider):
    management_logger: "ParseCommandLogger"
    name = "anibel_manga"

    def __init__(self, *args, logger, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update({"management_logger": logger})

    @property
    def logger(self):
        return self.management_logger

    def start_requests(self):
        self.logger.info("Starting requests")
        self.logger.info("=================")
        mangas_list = requests.get(f"{ANIBEL_URL}/manga")
        if not mangas_list.status_code == 200:
            self.logger.error(f"Failed request with code {mangas_list.status_code}")
            return
        mangas_list = mangas_list.text

        xpath_selector = '//li[@class = "page-item-num"]//a[@class = "page-link"]/text()'
        html_parser = etree.HTML(mangas_list)
        max_page = html_parser.xpath(xpath_selector)[-1]
        base_url = f"{ANIBEL_URL}/manga?page="
        pages = [page for page in range(1, int(max_page) + 1)]
        urls = [base_url + str(page) for page in pages]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def request_fallback(self, failure: Failure):
        self.logger.error(
            f'Request for url "{failure.value.response.url}" '
            f"failed with status {failure.value.response.status}"
        )

    def parse(self, response):
        mangas = []
        descriptions = response.xpath(MANGA_CARD_TAG).extract()
        for description in descriptions:
            response = HtmlResponse(url="", body=description, encoding="utf-8")

            full_title = response.xpath(TITLE_TAG).extract_first("")
            alt_title = full_title.split(" / ")[1]
            alt_title = alt_title.split("[")[0]
            title = full_title.split(" / ")[0]
            source_url = ANIBEL_URL + response.xpath(SOURCE_URL_TAG).extract_first("")
            genres = response.xpath(GENRES_TAG).extract()
            image = ANIBEL_URL + response.xpath(THUMBNAIL_IMG_URL_TAG).extract_first("")
            mangas.append(
                {
                    "title": title,
                    "alt_title": alt_title,
                    "thumbnail": image,
                    "genres": genres,
                    "image": image,
                    "source_url": source_url,
                }
            )
            self.logger.info('Parsed ,anga "{}"'.format(title))

        self.logger.info("Processing items...")
        self.logger.info("===================")
        return mangas
