from crochet import run_in_reactor, setup
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings

from apps.parse.const import CATALOGUES


def run(spider, *args, **kwargs):
    runner = CrawlerRunner(get_project_settings())
    return runner.crawl(spider, *args, **kwargs)


def run_parser(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    catalogue = CATALOGUES[catalogue_name]
    spider, wait_timeout = catalogue["parsers"][parser_type]

    if wait_timeout:
        setup()
        d = run_in_reactor(run)(spider, url=url)
        d.wait(wait_timeout)
    else:
        # Don't use reactor for spiders without timeout
        runner = CrawlerProcess(get_project_settings())
        runner.crawl(spider, url=url)
        runner.start()
