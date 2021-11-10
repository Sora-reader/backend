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
    # FKs
    chapters = Field()
    # M2Ms
    genres = Field()
    categories = Field()
    authors = Field()
    translators = Field()
    illustrators = Field()
    screenwriters = Field()
    # Other
    updated_detail = Field()


class MangaChapterItem(Item):
    title = Field()
    volume = Field()
    number = Field()
    link = Field()
