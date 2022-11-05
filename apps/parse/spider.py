from abc import ABC

import scrapy


class RegisteredSpider(scrapy.Spider, ABC):
    type: str


class BaseSpider(RegisteredSpider, ABC):
    pass
