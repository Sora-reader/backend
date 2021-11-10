from functools import partial

from django.conf import settings
from scrapy.http import Request
from scrapy.spiders import Spider
from twisted.python.failure import Failure


def errback(spider: Spider, failure: Failure = None, *args, **kwargs):
    spider.logger.warning(f"Error on {failure.response.url}\n{repr(failure)}")


class ErrbackMiddleware(object):
    def process_request(self, request: Request, spider: Spider, **_):
        if not request.errback:
            request.errback = partial(errback, spider)


class ProxyMiddleware(object):
    def process_request(self, request: Request, **_):
        request.meta["proxy"] = settings.PROXY
