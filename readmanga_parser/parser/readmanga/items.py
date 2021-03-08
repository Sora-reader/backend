# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Manga(scrapy.Item):
    name = Field()
    genres = Field()
    author = Field()
    chapters = Field()
    category = Field()
    status = Field()
    year = Field()
    translators = Field()
    description = Field()
