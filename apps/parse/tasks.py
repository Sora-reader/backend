from django.core.cache import caches
from django_rq import job
from scrapy.utils.project import get_project_settings
from scrapyscript import Job, Processor

from apps.parse.catalogue import Catalogue
from apps.parse.exceptions import ParsingError, to_error_schema
from apps.parse.types import CacheType, ParsingStatus


@job
def run_spider_task(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    catalogue = Catalogue.from_name(catalogue_name)
    spider = catalogue.from_parser_name(parser_type)
    cache = None

    j = Job(spider, url=url)
    p = Processor(settings=get_project_settings())

    if url:
        cache = caches[CacheType.from_parser_type(parser_type)]
        cache.set(url, ParsingStatus.parsing)

    p.run(j)

    if p.errors:
        errors = [f"{str(cls)}={val}" for cls, val in p.errors]
        msg = "Parsing failed with errors:\n" + "\n".join(errors)
        if url:
            cache.set(url, to_error_schema(msg))
        raise ParsingError(msg)

    if url:
        cache_res = cache.get(url)
        if cache_res == ParsingStatus.parsing.value:
            msg = "Parsing failed but returned no errors, please, try again later."
            cache.set(url, to_error_schema(msg))
            raise ParsingError(msg)
