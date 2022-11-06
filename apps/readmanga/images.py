import re

from orjson import loads
from scrapy.http import HtmlResponse

from apps.parse.exceptions import ParsingError
from apps.parse.scrapy.items import ImagesItem
from apps.parse.scrapy.spider import BaseSpider
from apps.parse.types import ParserType
from apps.readmanga import Readmanga

COUNT_LINK_ELEMENTS = 3


@Readmanga.register(ParserType.image)
class ReadmangaImageSpider(BaseSpider):
    custom_settings = {"ITEM_PIPELINES": {"apps.readmanga.pipelines.ReadmangaImagePipeline": 300}}

    def __init__(self, *args, url: str, **kwargs):
        super().__init__(*args, **kwargs, start_urls=[url])

    def parse(self, response: HtmlResponse, **kwargs):
        images = re.search(r"rm_h.initReader\(.*(\[{2}.*]{2}).*\)", response.text)
        if not images:
            raise ParsingError("No image list was found")

        image_links = [
            "".join(image[:COUNT_LINK_ELEMENTS])
            for image in loads(images.group(1).replace("'", '"'))
        ]
        return ImagesItem(chapter_url=self.start_urls[0], images=image_links)
