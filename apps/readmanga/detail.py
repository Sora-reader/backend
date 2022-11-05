from scrapy.http import HtmlResponse

from apps.core.utils import url_prefix
from apps.parse.const import ParserType
from apps.parse.scrapy.items import MangaItem
from apps.parse.spider import BaseSpider
from apps.readmanga import Readmanga

_identifier = "//span[contains(@class, 'rating-block')]/@data-subject-id"

_description = "//meta[@itemprop='description'][1]/@content"
_chapters_url = "//head/link[@type='application/rss+xml'][1]/@href"
_year = "//span[@class='elem_year ']/a[@class='element-link'][1]/text()"
_rating = "//span[@class='rating-block']/@data-score"

_categories = '//span[@class = "elem_category "]/a[@class="element-link"]/text()'

_authors = "//span[@class='elem_author ']/a[@class='person-link']/text()"
_translators = "//span[@class='elem_translator ']/a[@class='person-link']/text()"
_illustrators = '//span[@class = "elem_illustrator "]/a[@class="person-link"]/text()'
_screenwriters = '//span[@class="elem_screenwriter "]/a[@class="person-link"]/text()'


@Readmanga.register(ParserType.detail)
class ReadmangaDetailSpider(BaseSpider):
    def parse(self, response: HtmlResponse, **kwargs):
        identifier = response.xpath(_identifier).extract_first()

        description = response.xpath(_description).extract_first("")
        chapters_url = response.xpath(_chapters_url).extract_first("")
        year = response.xpath(_year).extract_first("")
        rating = response.xpath(_rating).extract_first(0.0)

        categories = response.xpath(_categories).extract()

        authors = response.xpath(_authors).extract()
        screenwriters = response.xpath(_screenwriters).extract()
        translators = response.xpath(_translators).extract()
        illustrators = response.xpath(_illustrators).extract()

        if chapters_url:
            chapters_url = url_prefix(self.start_urls[0]) + chapters_url

        return [
            MangaItem(
                identifier=identifier,
                description=description,
                source_url=response.url,
                chapters_url=chapters_url,
                year=year,
                rating=rating,
                categories=categories,
                authors=authors,
                translators=translators,
                illustrators=illustrators,
                screenwriters=screenwriters,
            )
        ]
