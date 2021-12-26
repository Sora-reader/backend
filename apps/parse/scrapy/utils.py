# from scrapy.crawler import CrawlerProcess, CrawlerRunner
# from crochet import run_in_reactor, wait_for, setup
# setup()

import scrapydo

from apps.parse.readmanga.chapter import ReadmangaChapterSpider

scrapydo.setup()


# @wait_for(10)
# def run(spider, url):
#     import time
#     time.sleep(2)
# process = CrawlerProcess(get_project_settings())
#     process = CrawlerRunner(get_project_settings())

#     process.crawl(spider, url=url)
# process.start()

# @run_in_reactor
def run_parser(parser_type: str, catalogue_name: str = "readmanga", url: str = None):
    # catalogue = CATALOGUES[catalogue_name]
    # spider = catalogue["parsers"][parser_type]

    scrapydo.crawl(
        url=url,
        callback=ReadmangaChapterSpider.parse,
        spider_cls=ReadmangaChapterSpider,
    )

    # try:
    # run(spider, url)
    # Avoid scrapy's signal
    # except ValueError:
    # pass
