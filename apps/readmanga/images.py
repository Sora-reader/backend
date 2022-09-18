import re

import scrapy
import ujson
from scrapy.http import HtmlResponse

from apps.core.utils import init_redis_client
from apps.parse.items import ImagesItem
from apps.parse.spider import InjectUrlMixin

COUNT_LINK_ELEMENTS = 3


class ReadmangaImageSpider(InjectUrlMixin, scrapy.Spider):
    name = "readmanga_image"
    custom_settings = {"ITEM_PIPELINES": {"apps.readmanga.pipelines.ReadmangaImagePipeline": 300}}
    url: str = None
    "Chapter url, like https://readmanga.live/podniatie_urovnia_v_odinochku__A5664/vol1/0"

    def __init__(self, *args, url: str, **kwargs):
        super().__init__(*args, **kwargs, start_urls=[url], redis_client=init_redis_client())

    def parse(self, response: HtmlResponse, **kwargs):
        images = re.search(r"rm_h.initReader\(.*(\[{2}.*]{2}).*\)", response.text)
        image_links = []
        if images:
            image_links = [
                "".join(image[:COUNT_LINK_ELEMENTS])
                for image in ujson.loads(images.group(1).replace("'", '"'))
            ]
        return ImagesItem(chapter_url=self.start_urls[0], images=image_links)
