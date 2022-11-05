from scrapy import Field, Item


class MangaItem(Item):
    identifier = Field()

    title = Field()
    description = Field()
    rating = Field()
    thumbnail = Field()
    image = Field()
    status = Field()
    year = Field()
    source_url = Field()
    chapters_url = Field()
    # FKs
    chapters = Field()
    # M2Ms
    genres = Field()
    categories = Field()
    # M2M persons
    authors = Field()
    translators = Field()
    illustrators = Field()
    screenwriters = Field()


class ChapterItem(Item):
    chapters = Field()
    # Meta
    chapters_url = Field()


class ImagesItem(Item):
    chapter_url = Field()
    images = Field()
