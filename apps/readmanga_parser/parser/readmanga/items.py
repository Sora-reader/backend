# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class MangaItem(Item):
    image_url = Field()
    title_url = Field()
    title = Field()
    genres = Field()
    description = Field()
