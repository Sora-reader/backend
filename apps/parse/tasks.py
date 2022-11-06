from django.core.cache import caches
from django_rq import job
from scrapy.utils.project import get_project_settings
from scrapyscript import Job, Processor

from apps.parse.catalogue import Catalogue
from apps.parse.exceptions import ParsingError, to_error_schema
from apps.parse.types import CacheType, ParsingStatus


@job
def run_spider_task(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    catalogue = Catalogue.get(catalogue_name)
    spider = catalogue.get_parser(parser_type)
    cache = caches[CacheType.from_parser_type(parser_type)]

    j = Job(spider, url=url)
    p = Processor(settings=get_project_settings())

    if url:
        cache.set(url, ParsingStatus.parsing)

    p.run(j)

    if p.errors:
        errors = [f"{str(cls)}={val}" for cls, val in p.errors]
        # errors = []
        msg = f"Parsing failed with errors:\n" + "\n".join(errors)
        cache.set(url, to_error_schema(msg))
        raise ParsingError(msg)

    if url:
        cache_res = cache.get(url)
        if cache_res == ParsingStatus.parsing.value:
            msg = f"Parsing failed but returned no errors, please, try again later."
            cache.set(url, to_error_schema(msg))
            raise ParsingError(msg)
