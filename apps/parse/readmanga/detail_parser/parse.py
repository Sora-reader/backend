import logging
from copy import deepcopy
from typing import Optional

import requests
from django.conf import settings
from django.utils import timezone
from scrapy.http.response.html import HtmlResponse

from apps.parse.models import Category, Manga, PersonRelatedToManga
from apps.parse.utils import needs_update, save_persons

from .consts import (
    AUTHORS_TAG,
    CATEGORY_TAG,
    DESCRIPTION_TAG,
    ILLUSTRATOR_TAG,
    RSS_TAG,
    SCREENWRITER_TAG,
    STAR_RATING_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)

INSTANCE = 0

logger = logging.getLogger("Detailed manga parser")


def get_detailed_info(url: str) -> dict:
    response = requests.get(url, headers=settings.HEADERS)
    if response.status_code != 200:
        raise Exception(response.text)
    manga_html = HtmlResponse(url="", body=response.text, encoding="utf-8")
    year = manga_html.xpath(YEAR_TAG).extract_first("")
    description = manga_html.xpath(DESCRIPTION_TAG).extract_first("")
    rating = manga_html.xpath(STAR_RATING_TAG).extract_first(0.0)
    rss_url = manga_html.xpath(RSS_TAG).extract_first("")
    authors = manga_html.xpath(AUTHORS_TAG).extract()
    screenwriters = manga_html.xpath(SCREENWRITER_TAG).extract()
    translators = manga_html.xpath(TRANSLATORS_TAG).extract()
    categories = manga_html.xpath(CATEGORY_TAG).extract()
    illustrators = manga_html.xpath(ILLUSTRATOR_TAG).extract()
    detailed_info = {
        "authors": authors,
        "year": year,
        "rating": rating,
        "description": description,
        "translators": translators,
        "illustrators": illustrators,
        "screenwriters": screenwriters,
        "categories": categories,
        "rss_url": rss_url,
    }
    return detailed_info


def save_detailed_manga_info(
    manga: Manga,
    **kwargs,
) -> None:
    if manga is None:
        return

    data = deepcopy(kwargs)

    authors = data.pop("authors", [])
    illustrators = data.pop("illustrators", [])
    screenwriters = data.pop("screenwriters", [])
    translators = data.pop("translators", [])
    categories = data.pop("categories", [])

    save_persons(manga, PersonRelatedToManga.Roles.author, authors)
    save_persons(manga, PersonRelatedToManga.Roles.illustrator, illustrators)
    save_persons(manga, PersonRelatedToManga.Roles.screenwriter, screenwriters)
    save_persons(manga, PersonRelatedToManga.Roles.translator, translators)

    categories = [
        Category.objects.get_or_create(name=category)[INSTANCE] for category in categories
    ]

    manga.categories.clear()
    manga.categories.set(categories)
    data["updated_detail"] = timezone.now()
    data["rss_url"] = manga.url_prefix + data.pop("rss_url", "")
    Manga.objects.filter(pk=manga.pk).update(**data)


def deepen_manga_info(id: int) -> Optional[dict]:
    manga = Manga.objects.get(pk=id)

    if needs_update(manga, "updated_detail") or True:
        url = manga.source_url
        info: dict = get_detailed_info(url)
        save_detailed_manga_info(manga=manga, **info)
        return info
