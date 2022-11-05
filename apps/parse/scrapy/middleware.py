from functools import partial

from django.conf import settings
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import Spider


class ErrorLoggerMiddleware(object):
    @staticmethod
    def error_logger(spider: Spider, failure: HttpError, *args, **kwargs):
        if hasattr(failure, "response"):
            url = failure.response.url
        else:
            url = failure.request.url  # noqa
        spider.logger.warning(f"Error on {url}\n{repr(failure)}")

    def process_request(self, request: Request, spider: Spider, **_):
        if not request.errback:
            request.errback = partial(self.error_logger, spider)


class ProxyMiddleware(object):
    @staticmethod
    def process_request(request: Request, **_):
        request.meta["proxy"] = settings.PROXY
