from scrapy import Field

from apps.parse.scrapy.items import MangaItem


class MangaDetailAndChaptersItem(MangaItem):
    # MangaChapterItem
    chapters = Field()
