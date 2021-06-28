import logging
import re

import requests
import scrapy
from lxml import etree
from scrapy.http import HtmlResponse
from twisted.python.failure import Failure

from apps.parse.readmanga.readmanga.spiders.consts import (
    ALT_TITLE_URL,
    DESC_TEXT_DESCRIPTOR,
    DESCRIPTIONS_DESCRIPTOR,
    GENRES_DESCRIPTOR,
    IMG_URL_DESCRIPTOR,
    SOURCE_URL_DESCRIPTOR,
    STAR_RATE_DESCRIPTOR,
    TITLE_DESCRIPTOR,
)

logging.getLogger(__name__)
READMANGA_URL = "https://readmanga.live"


class MangaSpider(scrapy.Spider):
    name = "manga"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("custom_logger", None):
            self.__dict__.update({"logger_": kwargs["custom_logger"] or self.logger})

    def start_requests(self):
        self.logger_.info("Starting requests")
        self.logger_.info("=================")
        mangas_list = requests.get(f"{READMANGA_URL}/list")
        if not mangas_list.status_code == 200:
            self.logger_.error(f"Failed rqeuest with code {mangas_list.status_code}")
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
        self.logger_.error(
            f'Request for url "{failure.value.response.url}" '
            f"failed with status {failure.value.response.status}"
        )

    def parse(self, response):
        mangas = []
        descriptions = response.xpath(DESCRIPTIONS_DESCRIPTOR).extract()
        for description in descriptions:
            response = HtmlResponse(url="", body=description, encoding="utf-8")

            title = response.xpath(TITLE_DESCRIPTOR).extract()[0]
            try:
                rating = round(
                    float(response.xpath(STAR_RATE_DESCRIPTOR).extract()[0].split(" из ")[0]), 2
                )
            except Exception:
                rating = 0
            source_url = response.xpath(SOURCE_URL_DESCRIPTOR).extract()[0]
            desc_text = re.sub(
                " +", " ", response.xpath(DESC_TEXT_DESCRIPTOR).extract_first("").strip("")
            )
            genres = response.xpath(GENRES_DESCRIPTOR).extract()
            thumbnail = response.xpath(IMG_URL_DESCRIPTOR).extract()[0]
            alt_title = (
                response.xpath(ALT_TITLE_URL).extract()[0]
                if response.xpath(ALT_TITLE_URL).extract()
                else ""
            )

            mangas.append(
                {
                    "title": title,
                    "alt_title": alt_title,
                    "rating": rating,
                    "thumbnail": thumbnail,
                    "description": desc_text,
                    "genres": genres,
                    "source_url": READMANGA_URL + source_url,
                }
            )
            self.logger_.info('Parsed manga "{}"'.format(title))

        self.logger_.info("Processing items...")
        self.logger_.info("===================")
        return mangas
