from celery import shared_task
from scrapy.utils.project import get_project_settings
from scrapyscript import Job, Processor

from apps.parse.parser import PARSERS


@shared_task
def run_spider_task(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    parser_map = PARSERS[catalogue_name]
    spider, _ = parser_map[parser_type]
    job = Job(spider, url=url)
    p = Processor(settings=get_project_settings())
    p.run(job)
