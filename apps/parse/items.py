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


class MangaChapterItem(Item):
    chapters = Field()
    # Meta
    rss_url = Field()


class ImagesItem(Item):
    chapter_url = Field()
    images = Field()
