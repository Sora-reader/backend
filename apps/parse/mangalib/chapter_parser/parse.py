import asyncio
import json
import re
from typing import List, Optional

from django.utils import timezone
from pyppeteer import launch
from scrapy.http import HtmlResponse

from apps.parse.models import Chapter, Manga
from apps.parse.utils import needs_update

INSTANCE = 0


async def get_chapters_info(url: str) -> dict:
    data = dict()
    browser = await launch({"headless": True, "args": ["--no-sandbox", "--disable-setuid-sandbox"]})
    page = await browser.newPage()
    await page.setJavaScriptEnabled(False)
    await page.goto(url, {"timeout": 0})
    body = await page.content()
    html_tree = HtmlResponse(url="", body=body, encoding="utf-8")
    chapter_data = html_tree.xpath("//head/script/text()").extract_first("")
    if not chapter_data:
        await browser.close()
        raise Exception("Chapter info not found")
    for line in chapter_data.strip().split("\n"):
        if result := re.search(r"window\.__DATA__ = ([^;]*)", line):
            data = json.loads(result.group(1))
            break
    chapters = data.get("chapters").get("list")
    return chapters


def save_chapters_manga_info(manga: Manga, volumes: List[dict]) -> None:
    if manga is None:
        return

    manga.chapters.clear()

    chapters = []
    for chapter_info in volumes:
        chapter_number = chapter_info.get("chapter_number")
        volume = chapter_info.get("chapter_volume")
        link = f"{manga.source_url}/v{volume}/c{chapter_number}"
        title = chapter_info.get("chapter_name", "")
        chapter, created = Chapter.objects.get_or_create(
            number=chapter_number,
            volume=volume,
            link=link,
        )
        # функцией get_or_create мы проверяем есть ли у нас уже такая глава
        # независимо от перевода и названия. Добавляем название отдельно, потому что
        # не во всех переводах есть название
        if created and not chapter.title and title:
            chapter.title = title
            chapter.save()
        if chapter not in chapters:
            chapters.append(chapter)
    manga.chapters.set(chapters)
    manga.updated_chapters = timezone.now()
    manga.save()


def chapters_manga_info(id: int) -> Optional[dict]:
    manga: Manga = Manga.objects.get(pk=id)

    if needs_update(manga, "updated_chapters"):
        url = f"{manga.source_url}?section=chapters"
        info: dict = asyncio.get_event_loop().run_until_complete(get_chapters_info(url))
        save_chapters_manga_info(manga=manga, volumes=info)
        return info
