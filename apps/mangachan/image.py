import re

from orjson import loads

from apps.mangachan import Mangachan
from apps.parse.scrapy.items import ImagesItem
from apps.parse.scrapy.spider import BaseSpider
from apps.parse.types import ParserType


@Mangachan.register(ParserType.image)
class MangachanImageSpider(BaseSpider):
    custom_settings = {"ITEM_PIPELINES": {"apps.mangachan.pipelines.MangachanImagePipeline": 300}}

    def parse(self, response, **kwargs):
        image_links = re.search(r'"fullimg":(\[.*\",?])', response.text).group(1)
        without_trailing_comma = re.sub(r",?]$", "]", image_links)
        image_links = loads(without_trailing_comma)
        # TODO: fix loggers in scrapy
        self.logger.info(f"Parsed {len(image_links)} image links")
        return ImagesItem(chapter_url=self.start_urls[0], images=image_links)
