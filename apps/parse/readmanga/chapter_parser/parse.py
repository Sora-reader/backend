import xml.etree.ElementTree as ET
from copy import deepcopy
from typing import Optional

import requests
from django.utils import timezone

from apps.parse.models import Chapter, Manga

from .consts import ITEM_TAG, LINK_TAG, TITLE_TAG

INSTANCE = 0


def get_chapters_info(url: str) -> dict:
    chapters_info = dict()
    response = requests.get(url)

    chapters_rss = ET.fromstring(response.text)
    items = chapters_rss.findall(ITEM_TAG)
    for item in items:
        link = item.find(LINK_TAG).text

        title = item.find(TITLE_TAG).text

        vol, chapter = link.split("/")[-2:]
        vol = int(vol.replace("vol", ""))

        if not chapters_info.get(vol):
            chapters_info[vol] = list()
        chapters_info[vol].append(
            {
                "title": title,
                "chapter": chapter,
                "link": link,
            }
        )
    return chapters_info


def save_chapters_manga_info(
    manga: Manga,
    **kwargs,
) -> None:
    if manga is None:
        return

    data = deepcopy(kwargs)
    volumes = data.pop("volumes")

    manga.volumes.clear()

    chapters = []
    for volume_number, chapters_info in volumes.items():
        for chapter in chapters_info:
            chapter, _ = Chapter.objects.get_or_create(
                title=chapter.get("title"),
                number=chapter.get("chapter"),
                link=chapter.get("link"),
                volume=volume_number,
            )
            chapters.append(chapter)

    manga.volumes.set(chapters)
    manga.updated_chapters = timezone.now()
    manga.save()


def needs_update(manga: Manga):
    if manga.updated_chapters:
        update_deadline = manga.updated_chapters + Manga.UPDATED_CHAPTER_FREQUENCY
        if not timezone.now() >= update_deadline:
            return False
    return True


def chapters_manga_info(id: int, logger) -> Optional[dict]:
    manga: Manga = Manga.objects.get(pk=id)

    if needs_update(manga):
        rss_url = manga.rss_url
        info: dict = get_chapters_info(rss_url)
        save_chapters_manga_info(manga=manga, volumes=info)
        return info
