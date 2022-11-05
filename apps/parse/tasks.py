from django.core.cache import caches
from django_rq import job
from scrapy.utils.project import get_project_settings
from scrapyscript import Job, Processor

from apps.parse.exceptions import ParsingError, to_error_schema
from apps.parse.parser import CACHES, PARSERS
from apps.parse.types import ParsingStatus

SAME_THREAD = False


@job
def run_spider_task(
    parser_type: str, catalogue_name: str = "readmanga", url: str = None, *args, **kwargs
):
    parser_map = PARSERS[catalogue_name]
    spider, _ = parser_map[parser_type]
    cache = caches[CACHES[parser_type]]

    if SAME_THREAD:
        from scrapy.crawler import CrawlerProcess

        p = CrawlerProcess(settings=get_project_settings())
        p.crawl(spider, url=url)
    else:
        j = Job(spider, url=url)
        p = Processor(settings=get_project_settings())

    if url:
        cache.set(url, ParsingStatus.parsing)

    if SAME_THREAD:
        p.start()
    else:
        p.run(j)

    if url:
        cache_res = cache.get(url)
        if cache_res == ParsingStatus.parsing.value:
            error = f"Parsing failed for url {url}, please, try again later."
            cache.set(url, to_error_schema(error))
            raise ParsingError(error)
