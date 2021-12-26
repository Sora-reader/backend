import re
from typing import List

import scrapy
from scrapy.http import XmlResponse

from apps.parse.scrapy.items import MangaChapterItem

ITEM_TAG = "//item"
LINK_TAG = 'guid[@isPermaLink="true"]/text()'
TITLE_TAG = ".//title/text()"


class ReadmangaChapterSpider(scrapy.Spider):
    name = "readmanga_chapter"
    custom_settings = {
        "ITEM_PIPELINES": {"apps.parse.readmanga.pipelines.ReadmangaChapterPipeline": 300}
    }

    # def __init__(self, *args, url: str):
    # super().__init__(*args, start_urls=[url])

    @staticmethod
    # def parse(self, response: XmlResponse) -> List[MangaChapterItem]:
    def parse(response: XmlResponse, *args, **kwargs) -> List[MangaChapterItem]:
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
                MangaChapterItem(
                    **{
                        "manga_rss_url": response.url,
                        "title": chapter_title,
                        "volume": volume,
                        "number": number,
                        "link": link,
                    }
                )
            )
        return chapters
