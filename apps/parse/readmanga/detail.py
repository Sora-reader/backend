import scrapy
from scrapy.http import HtmlResponse

from apps.parse.scrapy.items import MangaItem

RSS_TAG = "//head/link[@type='application/rss+xml'][1]/@href"
AUTHORS_TAG = "//span[@class='elem_author ']/a[@class='person-link']/text()"
YEAR_TAG = "//span[@class='elem_year ']/a[@class='element-link'][1]/text()"
TRANSLATORS_TAG = "//span[@class='elem_translator ']/a[@class='person-link']/text()"
ILLUSTRATOR_TAG = '//span[@class = "elem_illustrator "]/a[@class="person-link"]/text()'
SCREENWRITER_TAG = '//span[@class="elem_screenwriter "]/a[@class="person-link"]/text()'
CATEGORY_TAG = '//span[@class = "elem_category "]/a[@class="element-link"]/text()'
DESCRIPTION_TAG = "//meta[@itemprop='description'][1]/@content"
STAR_RATING_TAG = "//span[@class='rating-block']/@data-score"


class ReadmangaDetailSpider(scrapy.Spider):
    name = "readmanga_detail"

    def __init__(self, *, url: str):
        self.start_urls = [url]

    def parse(self, response: HtmlResponse):
        year = response.xpath(YEAR_TAG).extract_first("")
        description = response.xpath(DESCRIPTION_TAG).extract_first("")
        rating = response.xpath(STAR_RATING_TAG).extract_first(0.0)
        rss_url = response.xpath(RSS_TAG).extract_first("")
        authors = response.xpath(AUTHORS_TAG).extract()
        screenwriters = response.xpath(SCREENWRITER_TAG).extract()
        translators = response.xpath(TRANSLATORS_TAG).extract()
        categories = response.xpath(CATEGORY_TAG).extract()
        illustrators = response.xpath(ILLUSTRATOR_TAG).extract()
        return [
            MangaItem(
                **{
                    "source_url": self.start_urls[0],
                    "authors": authors,
                    "year": year,
                    "rating": rating,
                    "description": description,
                    "translators": translators,
                    "illustrators": illustrators,
                    "screenwriters": screenwriters,
                    "categories": categories,
                    "rss_url": rss_url,
                }
            )
        ]
