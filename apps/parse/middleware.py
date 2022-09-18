from functools import partial

from django.conf import settings
from scrapy.http import Request
from scrapy.spiders import Spider


class ErrorLoggerMiddleware(object):
    @staticmethod
    def error_logger(spider: Spider, failure, *args, **kwargs):
        spider.logger.warning(f"Error on {failure.response.url}\n{repr(failure)}")

    def process_request(self, request: Request, spider: Spider, **_):
        if not request.errback:
            request.errback = partial(self.error_logger, spider)


class ProxyMiddleware(object):
    @staticmethod
    def process_request(request: Request, **_):
        request.meta["proxy"] = settings.PROXY
