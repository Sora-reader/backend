import re
from typing import List

import scrapy
import ujson
from scrapy.http import HtmlResponse

from apps.core.utils import init_redis_client
from apps.parse.models import Manga

COUNT_LINK_ELEMENTS = 3


class ReadmangaImageSpider(scrapy.Spider):
    name = "readmanga_image"
    custom_settings = {
        "ITEM_PIPELINES": {"apps.parse.readmanga.pipelines.ReadmangaImagePipeline": 300}
    }

    def __init__(self, *, url: str):
        self.start_urls = [url]
        self.redis_client = init_redis_client()

    @staticmethod
    def find_images(html: str) -> List[str]:
        image_links = []
        image_hints = re.search(r"rm_h.initReader\(.*(\[{2}.*\]{2}).*\)", html)
        if image_hints:
            image_links = [
                "".join(image[:COUNT_LINK_ELEMENTS])
                for image in ujson.loads(image_hints.group(1).replace("'", '"'))
            ]
        return image_links

    def parse(self, response: HtmlResponse):
        html_response = response.text
        images = self.find_images(html_response)

        self.redis_client.delete(response.url)
        if images:
            self.redis_client.rpush(response.url, *images)
        self.redis_client.expire(response.url, Manga.IMAGE_UPDATE_FREQUENCY)

        return images
