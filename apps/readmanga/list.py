import re
from typing import List

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from apps.core.utils import url_prefix
from apps.parse.items import MangaItem
from apps.parse.source import CATALOGUES
from apps.parse.spider import InjectUrlMixin

READMANGA_URL = CATALOGUES["readmanga"]["source"]
LIST_URL = f"{READMANGA_URL}/list"

_manga_tile = '//div[@class = "tiles row"]//div[contains(@class, "tile col-md-6")]'
_identifier = '//div[contains(@class, "tile col-md-6 ")]/@class'

_title = "//h3/a[1]/@title"
_thumbnail = '//img[contains(@class, "lazy")][1]/@data-original'
_source_url = "//h3/a[1]/@href"
_rating = '//div[@class = "compact-rate"]/@title'
_genres = '//div[@class = "tile-info"]//a[contains(@class, "badge")]/text()'


# Not used for now
# ALT_TITLE_URL = "//h4[@title]//text()"


class ReadmangaListSpider(InjectUrlMixin, CrawlSpider):
    name = "readmanga_list"
    start_urls = [LIST_URL]
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
        descriptions = response.xpath(_manga_tile).extract()
        for description in descriptions:
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
