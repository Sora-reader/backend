import scrapy
from scrapy import item
from ..readmanga_map import get_manga_urls
from scrapy.selector import Selector
from readmanga.items import Manga


class QuotesSpider(scrapy.Spider):
    name = 'manga'

    def start_requests(self):
        urls = get_manga_urls()[:50]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        name_tag = '//span[@class = "name"]/text()'
        genres_tag = '//p[@class = "elementList"]/span[@class = "elem_genre "]/a[@class = "element-link"]/text()'

        manga = Manga()
        manga['name'] = response.xpath(name_tag).extract()[0]
        manga['genres'] = response.xpath(genres_tag).extract()

        return manga
