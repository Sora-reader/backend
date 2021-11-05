from django.conf import settings
from scrapy.http import HtmlResponse, Request
from scrapy.spiders import Spider


def errback(spider: Spider, response: HtmlResponse):
    spider.logger.warning(f"Error on {response.url} ({response.status})\n{response.text}")


class ErrbackMiddleware(object):
    def process_request(self, request: Request, **_):
        if not request.errback:
            request.errback = errback


class ProxyMiddleware(object):
    def process_request(self, request: Request, **_):
        request.meta["proxy"] = settings.PROXY
