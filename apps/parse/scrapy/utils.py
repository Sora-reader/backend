from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from apps.parse.const import CATALOGUES


def run_parser(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    catalogue = CATALOGUES[catalogue_name]
    spider = catalogue["parsers"][parser_type]

    process = CrawlerProcess(get_project_settings())

    process.crawl(spider, url=url)
    process.start()
