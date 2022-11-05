import re

from scrapy.http import XmlResponse

from apps.parse.const import ParserType
from apps.parse.scrapy.items import ChapterItem
from apps.parse.spider import BaseSpider
from apps.readmanga import Readmanga

ITEM_TAG = "//item"
LINK_TAG = 'guid[@isPermaLink="true"]/text()'
TITLE_TAG = ".//title/text()"


@Readmanga.register(ParserType.chapter)
class ReadmangaChapterSpider(BaseSpider):
    custom_settings = {"ITEM_PIPELINES": {"apps.readmanga.pipelines.ReadmangaChapterPipeline": 300}}

    def parse(self, response: XmlResponse, **kwargs) -> ChapterItem:
        chapters = []

        items = response.xpath(ITEM_TAG)
        for item in items:
            link = item.xpath(LINK_TAG).extract_first()

            chapter_title = item.xpath(TITLE_TAG).extract_first()

            res_reg = re.search(r":\s*(.*)$", chapter_title)
            if res_reg:
                chapter_title = res_reg.group(1)

            volume, number = link.split("/")[-2:]
            volume = int(volume.replace("vol", ""))

            chapters.append(
                dict(
                    title=chapter_title,
                    volume=volume,
                    number=number,
                    link=link,
                )
            )
        return ChapterItem(chapters=chapters, chapters_url=response.url)
