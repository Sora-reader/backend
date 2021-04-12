from scrapy.item import Field, Item


class MangaItem(Item):
    image_url = Field()
    title_url = Field()
    title = Field()
    genres = Field()
    description = Field()
