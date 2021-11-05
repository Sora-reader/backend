from scrapy import Field, Item


class MangaItem(Item):
    title = Field()
    alt_title = Field()
    rating = Field()
    thumbnail = Field()
    image = Field()
    description = Field()
    status = Field()
    year = Field()
    source_url = Field()
    rss_url = Field()
    chapters = Field()
    genres = Field()
    categories = Field()
