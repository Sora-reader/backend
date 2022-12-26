import re
from typing import List

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from apps.core.utils import url_prefix
from apps.parse.scrapy.items import MangaItem
from apps.parse.scrapy.spider import BaseSpider
from apps.parse.types import ParserType
from apps.readmanga import Readmanga

_manga_tile = '//div[@class = "tiles row"]//div[contains(@class, "tile col-md-6")]'
_identifier = '//div[contains(@class, "tile col-md-6 ")]/@class'

_title = "//h3/a[1]/@title"
_thumbnail = '//img[contains(@class, "lazy")][1]/@data-original'
_source_url = "//h3/a[1]/@href"
_rating = '//div[@class = "compact-rate"]/@title'
_genres = '//div[@class = "tile-info"]//a[contains(@class, "badge")]/text()'


@Readmanga.register(ParserType.list, url=False)
class ReadmangaListSpider(CrawlSpider, BaseSpider):
    start_urls = [f"{Readmanga.source}/list?sortType=rate"]
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths=["//a[@class='nextLink']"]), follow=True, callback="parse"
        )
    ]
    custom_settings = {
        "DEPTH_LIMIT": 400,
    }

    def parse_start_url(self, response, **kwargs):
        return self.parse(response)

    def parse(self, response, **kwargs):
        mangas: List[MangaItem] = []

        url_offset = re.findall(r"offset=(\d+)", response.url)
        offset = int(url_offset[-1]) if url_offset else 0

        descriptions = response.xpath(_manga_tile).extract()
        for popularity, description in enumerate(descriptions, offset + 1):
            response = HtmlResponse(url="", body=description, encoding="utf-8")

            identifier = response.xpath(_identifier).extract_first()

            title = response.xpath(_title).extract_first("")
            thumbnail = response.xpath(_thumbnail).extract_first("")
            source_url = response.xpath(_source_url).extract_first("")
            rating = response.xpath(_rating).extract_first("")
            genres = response.xpath(_genres).extract()

            # Post-processing
            identifier = re.match(r".*el_(\d+).*", identifier).group(1)
            image = thumbnail.replace("_p", "")

            if not source_url.startswith("http"):
                source_url = url_prefix(self.start_urls[0]) + source_url

            mangas.append(
                MangaItem(
                    identifier=identifier,
                    popularity=popularity,
                    title=title,
                    thumbnail=thumbnail,
                    image=image,
                    source_url=source_url,
                    rating=rating,
                    genres=genres,
                )
            )
            self.logger.info('Parsed manga "{}"'.format(title))

        self.logger.info("===================")
        return mangas
