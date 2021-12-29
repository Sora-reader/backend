import scrapydo

from apps.parse.const import CATALOGUES, LIST_PARSER

scrapydo.setup()


def run_parser(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    catalogue = CATALOGUES[catalogue_name]
    spider = catalogue["parsers"][parser_type]
    if parser_type == LIST_PARSER:
        url = spider.start_urls[0]

    scrapydo.crawl(
        url=url,
        callback=spider.callback,
        spider_cls=spider,
    )
