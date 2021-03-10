from django.core.management.base import BaseCommand
from scrapy.utils.project import get_project_settings
from readmanga_parser.parser.readmanga.spiders.manga_spider import QuotesSpider
from scrapy.crawler import CrawlerProcess
import os

SETTINGS_PATH = 'readmanga_parser.parser.readmanga.settings'


class Command(BaseCommand):
    help = "Parse readmanga"

    def handle(self, *args, **options):
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', SETTINGS_PATH)
        process = CrawlerProcess(get_project_settings())

        process.crawl(QuotesSpider)
        process.start()
