import re

import scrapy
import ujson
from scrapy.http import HtmlResponse

from apps.core.utils import init_redis_client

COUNT_LINK_ELEMENTS = 3


class ReadmangaImageSpider(scrapy.Spider):
    name = "readmanga_image"
    custom_settings = {
        "ITEM_PIPELINES": {"apps.parse.readmanga.pipelines.ReadmangaImagePipeline": 300}
    }

    def __init__(self, *, url: str):
        self.start_urls = [url]
        self.redis_client = init_redis_client()

    def parse(self, response: HtmlResponse):
        images = re.search(r"rm_h.initReader\(.*(\[{2}.*\]{2}).*\)", response.text)
        if images:
            image_links = [
                "".join(image[:COUNT_LINK_ELEMENTS])
                for image in ujson.loads(images.group(1).replace("'", '"'))
            ]
        return {self.start_urls[0]: image_links}
