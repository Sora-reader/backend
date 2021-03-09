from django.core.management.base import BaseCommand
from readmanga_parser.parser.readmanga.spiders.manga_spider import QuotesSpider
from scrapy.crawler import CrawlerProcess


class Command(BaseCommand):
    help = "Parse readmanga"

    def handle(self, *args, **options):
        process = CrawlerProcess(settings={
            "FEEDS": {
                "items.json": {"format": "json"},
            }
        })

        process.crawl(QuotesSpider)
        process.start()
