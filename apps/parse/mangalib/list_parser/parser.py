import asyncio
import logging

from asgiref.sync import sync_to_async
from pyppeteer import launch, page
from scrapy.http import HtmlResponse

from apps.core.abc.commands import ParseCommandLogger
from apps.parse.models import Manga
from manga_reader.settings import DEFAULT_LAUNCH_ARGS

from .consts import CARDS_TAG, IMAGE_TAG, SOURCE_TAG, STATUS_CODE_TAG, TITLE_TAG

logging.getLogger(__name__)
MANGALIB_SOURCE = "https://mangalib.me"


class Crawler:
    def __init__(
        self,
        logger: "ParseCommandLogger",
        max_workers: int = 3,
    ):
        self.max_workers = max_workers
        self.task_queued = 0
        self.continue_parse = True
        self.mangas = []
        self.__dict__.update({"management_logger": logger})

    @property
    def logger(self):
        return self.management_logger

    async def get_list(self):
        self.logger.info("Starting list parser")
        self.logger.info("=====================")
        self.browser = await launch(DEFAULT_LAUNCH_ARGS)
        workers = asyncio.gather(
            *[
                self._worker(await self.browser.newPage(), worker_num)
                for worker_num in range(self.max_workers)
            ]
        )
        await workers
        await self.bulk_create_mangas()

        await self.browser.close()

    @sync_to_async
    def bulk_create_mangas(self):
        Manga.objects.bulk_create(
            [
                Manga(
                    **manga,
                )
                for manga in self.mangas
            ],
            ignore_conflicts=True,
        )

    async def _worker(self, page: page.Page, worker_num: int):
        self.logger.info(f"Starting worker # {worker_num}")
        await page.setJavaScriptEnabled(False)
        while self.continue_parse:
            self.task_queued += 1
            page_num = self.task_queued
            await self.parse_page(page, page_num)

    async def parse_page(self, page: page.Page, page_num: int):
        full_url = "https://mangalib.me/manga-list?page={}".format(page_num)
        await page.goto(full_url, {"timeout": 0})
        text_body = await page.content()

        html_body = HtmlResponse(url="", body=text_body, encoding="utf-8")

        if self.page_has_500_code(html_body, full_url):
            self.logger.error(f"Page {full_url} returned 500 status")
            self.continue_parse = False

        self.get_mangas_info(html_body)

    def page_has_500_code(self, page_html, full_url):
        return bool(page_html.xpath(STATUS_CODE_TAG).extract_first(""))

    def get_mangas_info(self, page_html):
        cards = page_html.xpath(CARDS_TAG).extract()
        for html_card in cards:
            manga_card = HtmlResponse(url="", body=html_card, encoding="utf-8")

            title = manga_card.xpath(TITLE_TAG).extract_first("")
            source_url = manga_card.xpath(SOURCE_TAG).extract_first("")
            image = manga_card.xpath(IMAGE_TAG).extract_first("")
            self.mangas.append(
                {
                    "title": title,
                    "image": MANGALIB_SOURCE + image,
                    "thumbnail": MANGALIB_SOURCE + image,
                    "source_url": source_url,
                }
            )
            self.logger.info(f"Parsed manga `{title}`")
