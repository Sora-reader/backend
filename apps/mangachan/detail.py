import re

from scrapy.http import HtmlResponse

from apps.core.utils import url_prefix
from apps.mangachan import Mangachan
from apps.parse.scrapy.items import ChapterItem, MangaItem
from apps.parse.scrapy.spider import BaseSpider
from apps.parse.types import ParserType


def clear_description(desc):
    escapes = "".join([chr(char) for char in range(1, 32)])
    translator = str.maketrans("", "", escapes)
    return desc.translate(translator).replace("  ", "").strip(" ")


@Mangachan.register(ParserType.detail)
class MangachanDetailSpider(BaseSpider):
    custom_settings = {
        "ITEM_PIPELINES": {
            "apps.mangachan.pipelines.MangachanPipeline": 300,
            "apps.mangachan.pipelines.MangachanChapterPipeline": 310,
        }
    }

    def parse(self, response: HtmlResponse, **kwargs):
        identifier = response.url[len(url_prefix(response.url)) :]

        description = response.xpath('//div[@id="description"]/text()').extract_first()

        trs = response.xpath("//table[@class='mangatitle']//tr").extract()

        other_fields = {}
        for row in trs:
            row = HtmlResponse(url="", body=row, encoding="utf-8")

            name_var_map = {
                "Тип": "categories",
                "Автор": "authors",
                "Тэги": "genres",
                "Переводчики": "translators",
            }
            name = row.xpath("//td/text()").extract_first()
            data = row.xpath("//td//a/text()").extract()

            field = name_var_map.get(name, None)
            if field:
                other_fields[field] = data

        description = clear_description(description)

        chapters = []
        for row in response.xpath('//div[@class="manga2"]/a'):
            name = row.xpath("text()").extract_first()
            link = row.xpath("@href").extract_first()

            if not link.startswith("http"):
                link = url_prefix(response.url) + link

            volume, number, title = re.match(
                r"^Том\s*(\d+)\s*Глава\s*([\d.]+)\s*(.*)\w*$", name
            ).groups()

            chapters.append(
                dict(
                    volume=volume,
                    number=number,
                    title=title,
                    link=link,
                )
            )

        return [
            MangaItem(
                identifier=identifier,
                description=description,
                source_url=response.url,
                **other_fields,
                chapters=ChapterItem(chapters=chapters, chapters_url=response.url),
            )
        ]
