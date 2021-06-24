from scrapy.item import Field, Item


class MangaItem(Item):
    image_url = Field()
    title_url = Field()
    title = Field()
    genres = Field()
    description = Field()
    alt_title = Field()
    source = Field()


class DetailMangaItem(Item):
    alt_title = Field()
    category = Field()
    year = Field()
    illustrators = Field()
    screenwriters = Field()
    authors = Field()
    rss_link = Field()
