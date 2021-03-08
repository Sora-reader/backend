# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Manga(scrapy.Item):
    name = Field()
    genres = Field()
    chapters = Field()
    category = Field()
    status = Field()
    year = Field()


class NewItem(scrapy.Item):

    main_headline = Field()
    headline = Field()

    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()


class TestItem(scrapy.Item):
    id = Field()
    name = Field()
    description = Field()
