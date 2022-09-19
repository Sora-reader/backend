from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apps.parse.parser import PARSERS


def run_parser(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    parser_map = PARSERS[catalogue_name]
    spider, _ = parser_map[parser_type]

    runner = CrawlerProcess(get_project_settings())
    runner.crawl(spider, url=url)
    runner.start()
