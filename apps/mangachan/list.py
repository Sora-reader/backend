from typing import List

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from apps.core.utils import url_prefix
from apps.mangachan import Mangachan
from apps.parse.scrapy.items import MangaItem
from apps.parse.scrapy.spider import BaseSpider
from apps.parse.types import ParserType

_manga_tile = '//div[@class = "content_row"]'

_title_selector = "//a[@class = 'title_link']"
_thumbnail = "//div[@class = 'manga_images']//img/@src"
_genres = "//div[@class = 'genre']/a/text()"


@Mangachan.register(ParserType.list, url=False)
class MangachanListSpider(BaseSpider, CrawlSpider):
    start_urls = [f"{Mangachan.source}/catalog"]
    rules = [
        Rule(
            LinkExtractor(
                restrict_xpaths=["//div[@id='pagination']/a[contains(text(), 'Вперед')]"],
            ),
            follow=True,
            callback="parse",
        )
    ]
    custom_settings = {
        "DEPTH_LIMIT": 1500,
    }

    def parse_start_url(self, response, **kwargs):
        return self.parse(response)

    def parse(self, response, **kwargs):
        mangas: List[MangaItem] = []
        descriptions = response.xpath(_manga_tile).extract()
        for description in descriptions:
            response = HtmlResponse(url="", body=description, encoding="utf-8")

            title_selector = response.xpath(_title_selector)
            title = title_selector.xpath("text()").extract_first()
            identifier = title_selector.xpath("@href").extract_first()

            thumbnail = response.xpath(_thumbnail).extract_first()
            image = thumbnail

            source_url = identifier
            rating = None

            genres = response.xpath(_genres).extract()

            if not source_url.startswith("http"):
                source_url = url_prefix(self.start_urls[0]) + source_url

            mangas.append(
                MangaItem(
                    identifier=identifier,
                    title=title,
                    thumbnail=thumbnail,
                    image=image,
                    source_url=source_url,
                    chapters_url=source_url,
                    rating=rating,
                    genres=genres,
                )
            )
            self.logger.info('Parsed manga "{}"'.format(title))

        self.logger.info("===================")
        return mangas
