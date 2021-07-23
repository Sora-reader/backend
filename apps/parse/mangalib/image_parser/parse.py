import asyncio
import json
from typing import List

from pyppeteer.launcher import launch
from scrapy.http import HtmlResponse

from apps.core.utils import init_redis_client
from apps.parse.mangalib.image_parser.consts import PAGE_TAG, SCRIPT_SERVER_TAG
from apps.parse.models import Chapter


def find_images(html: str) -> List[str]:
    html_tree = HtmlResponse(url="", body=html, encoding="utf-8")

    pg_elem = html_tree.xpath(PAGE_TAG).extract_first("")
    start_pos = pg_elem.find("=") + 2
    end_pos = pg_elem.find(";")
    pages = json.loads(pg_elem[start_pos:end_pos])

    script_elem = html_tree.xpath(SCRIPT_SERVER_TAG).extract()[-1]
    for line in script_elem.strip().split("\n"):
        if line.strip().startswith("window.__info"):
            start_pos = line.find("=") + 2
            end_pos = line.find(";")
            server_data = json.loads(line[start_pos:end_pos])
            break
    domain = server_data.get("servers").get("main")
    url = server_data.get("img").get("url")

    image_links = []
    for page in pages:
        image_links.append(f"{domain}/{url}{page.get('u')}")
    return image_links


async def parse_new_images(url: str, redis_client) -> List[str]:
    browser = await launch({"headless": True, "args": ["--no-sandbox", "--disable-setuid-sandbox"]})
    page = await browser.newPage()
    await page.setJavaScriptEnabled(False)
    await page.goto(url, {"timeout": 0})
    body = await page.content()
    images = []

    images = find_images(body)

    redis_client.delete(url)
    redis_client.rpush(url, *images)

    return images


def parse_images(url: str) -> List[str]:
    redis_client = init_redis_client()
    images = redis_client.lrange(url, 0, -1)
    if not images:
        images = asyncio.get_event_loop().run_until_complete(parse_new_images(url, redis_client))
    return images


def images_manga_info(chapter: Chapter) -> List[str]:
    return parse_images(chapter.link)
