from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings

from apps.parse.parser import PARSERS


def run(spider, *args, **kwargs):
    runner = CrawlerRunner(get_project_settings())
    return runner.crawl(spider, *args, **kwargs)


def run_parser(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    parser_map = PARSERS[catalogue_name]
    spider, _ = parser_map[parser_type]

    # Don't use reactor for spiders without timeout
    runner = CrawlerProcess(get_project_settings())
    runner.crawl(spider, url=url)
    runner.start()
