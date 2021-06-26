import datetime as dt
import logging
import xml.etree.ElementTree as ET
from typing import Optional

import pytz
import requests

from apps.parse.models import Manga

from .consts import LINK_TAG

INSTANCE = 0

logger = logging.getLogger("Chapters manga parser")


def get_chapters_info(url: str) -> dict:
    chapters_info = dict()
    response = requests.get(url)

    chapters_rss = ET.fromstring(response.text)
    links: list[str] = [elem.text for elem in chapters_rss.findall(LINK_TAG)]
    for link in links:
        vol, chapter = link.split("/")[-2:]
        vol = int(vol.replace("vol", ""))
        if not chapters_info.get(vol):
            chapters_info[vol] = list()
        chapters_info[vol].append(chapter)

    return chapters_info


def save_chapters_manga_info(
    manga: Manga,
    volumes: dict,
) -> None:
    if manga is None:
        return

    manga.volumes = volumes
    manga.updated_chapters = dt.datetime.now(pytz.UTC)
    manga.save()


def is_need_update(manga: Manga):
    if manga.updated_chapters:
        update_deadline = manga.updated_chapters + dt.timedelta(minutes=30)
        if dt.datetime.now(pytz.UTC) >= update_deadline:
            return True
        else:
            logger.info(f"Manga {manga.alt_title} is already up to date")
            return False
    else:
        return True


def chapters_manga_info(id: int) -> Optional[dict]:
    manga: Manga = Manga.objects.filter(pk=id).first()
    if manga is None:
        logger.error("Manga not found")
        return

    if not is_need_update(manga):
        return

    rss_url = manga.rss_url
    info: dict = get_chapters_info(rss_url)
    save_chapters_manga_info(manga=manga, volumes=info)
    logger.info(f"Successful parsing chapters of manga {manga.alt_title}")
    return info
