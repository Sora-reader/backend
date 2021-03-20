# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class MangaItem(Item):
    year = Field()
    image = Field()
    author = Field()
    manga = Field()
    name = Field()
    genres = Field()
    translators = Field()
    description = Field()
