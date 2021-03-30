import logging
import time

import requests
import scrapy
from lxml import etree
from scrapy.http import HtmlResponse

from apps.readmanga_parser.parser.readmanga.items import MangaItem
from apps.readmanga_parser.parser.readmanga.spiders.consts import (
    DESC_TEXT_DESCRIPTOR,
    DESCRIPTIONS_DESCRIPTOR,
    GENRES_DESCRIPTOR,
    IMG_URL_DESCRIPTOR,
    TITLE_DESCRIPTOR,
)
from apps.readmanga_parser.parser.readmanga.spiders.utils import extract_description

logging.getLogger(__name__)


class MangaSpider(scrapy.Spider):
    name = "manga"

    def start_requests(self):
        mangas_list = requests.get("https://readmanga.live/list").text

        xpath_selector = '//a[@class = "step"]/text()'
        html_parser = etree.HTML(mangas_list)
        maximum_page = html_parser.xpath(xpath_selector)[-1]
        standart_offset = 70
        maximum_offset = (int(maximum_page) - 1) * standart_offset

        base_url = "https://readmanga.live/list?&offset="
        offsets = [offset for offset in range(0, maximum_offset, standart_offset)]
        urls = [base_url + str(offset) for offset in offsets]

        for url in urls:
            time.sleep(2)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        mangas = []
        descriptions = response.xpath(DESCRIPTIONS_DESCRIPTOR).extract()
        for description in descriptions:
            manga = MangaItem()
            response = HtmlResponse(url="", body=description, encoding="utf-8")
            title = response.xpath(TITLE_DESCRIPTOR).extract()[0]
            # this is neccesary due to cleanse description from garbage
            desc_text = extract_description(response, DESC_TEXT_DESCRIPTOR)
            genres = response.xpath(GENRES_DESCRIPTOR).extract()
            image_url = response.xpath(IMG_URL_DESCRIPTOR).extract()[0]

            manga["genres"] = genres
            manga["description"] = desc_text
            manga["title"] = title
            manga["image_url"] = image_url

            mangas.append(manga)

        return mangas
