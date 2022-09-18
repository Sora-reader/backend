import re
from typing import List

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from apps.parse.items import MangaItem
from apps.parse.source import CATALOGUES
from apps.parse.spider import InjectUrlMixin

READMANGA_URL = CATALOGUES["readmanga"]["source"]
LIST_URL = f"{READMANGA_URL}/list"

MANGA_TILE_TAG = '//div[@class = "tiles row"]//div[contains(@class, "tile col-md-6")]'
STAR_RATE_TAG = '//div[@class = "rating"]/@title'
TITLE_TAG = "//h3/a[1]/@title"
SOURCE_URL_TAG = "//h3/a[1]/@href"
GENRES_TAG = '//div[@class = "tile-info"]//a[contains(@class, "badge")]/text()'
THUMBNAIL_IMG_URL_TAG = '//img[contains(@class, "lazy")][1]/@data-original'
ALT_TITLE_URL = "//h4[@title]//text()"


def parse_rating(rate_str: str):
    """
    >>> parse_rating("9.439212799072266 из 10")
    9.43
    """
    try:
        return float(re.match(r"^(\d\.\d{2})\d* из 10$", rate_str).group(1))
    except (AttributeError, ValueError):
        return 0.0


class ReadmangaListSpider(InjectUrlMixin, CrawlSpider):
    name = "readmanga_list"
    start_urls = [LIST_URL]
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths=["//a[@class='nextLink']"]),
            follow=True,
            callback="parse",
        ),
    ]
    custom_settings = {
        "DEPTH_LIMIT": 400,
    }

    def parse_start_url(self, response, **kwargs):
        return self.parse(response)

    def parse(self, response, **kwargs):
        mangas: List[MangaItem] = []
        descriptions = response.xpath(MANGA_TILE_TAG).extract()
        for description in descriptions:
            response = HtmlResponse(url="", body=description, encoding="utf-8")

            rating = parse_rating(response.xpath(STAR_RATE_TAG).extract_first("")) / 2
            title = response.xpath(TITLE_TAG).extract_first("")
            source_url = response.xpath(SOURCE_URL_TAG).extract_first("")
            genres = response.xpath(GENRES_TAG).extract()
            thumbnail = response.xpath(THUMBNAIL_IMG_URL_TAG).extract_first("")
            image = thumbnail.replace("_p", "")
            alt_title = response.xpath(ALT_TITLE_URL).extract_first("")

            mangas.append(
                MangaItem(
                    **{
                        "rating": rating,
                        "title": title,
                        "alt_title": alt_title,
                        "thumbnail": thumbnail,
                        "image": image,
                        "genres": genres,
                        "source_url": READMANGA_URL + source_url,
                    }
                )
            )
            self.logger.info('Parsed manga "{}"'.format(title))

        self.logger.info("===================")
        return mangas
