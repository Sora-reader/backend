import datetime as dt
import logging
from typing import Optional

import pytz
import requests
from scrapy.http.response.html import HtmlResponse

from apps.parse.models import Category, Manga, Person, PersonRelatedToManga

from .consts import (
    AUTHORS_TAG,
    CATEGORY_TAG,
    DESCRIPTION_TAG,
    ILLUSTRATOR_TAG,
    RSS_TAG,
    SCREENWRITER_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)

INSTANCE = 0

logger = logging.getLogger("Detailed manga parser")


def get_detailed_info(url: str) -> dict:
    response = requests.get(url)
    manga_html = HtmlResponse(url="", body=response.text, encoding="utf-8")

    year = manga_html.xpath(YEAR_TAG).extract_first("")
    description = manga_html.xpath(DESCRIPTION_TAG).extract_first("")
    rss_url = manga_html.xpath(RSS_TAG).extract_first("")
    authors = manga_html.xpath(AUTHORS_TAG).extract()
    screenwriters = manga_html.xpath(SCREENWRITER_TAG).extract()
    translators = manga_html.xpath(TRANSLATORS_TAG).extract()
    categories = manga_html.xpath(CATEGORY_TAG).extract()
    illustrators = manga_html.xpath(ILLUSTRATOR_TAG).extract()

    detailed_info = {
        "authors": authors,
        "year": year,
        "description": description,
        "translators": translators,
        "illustrators": illustrators,
        "screenwriters": screenwriters,
        "categories": categories,
        "rss_url": rss_url,
    }
    return detailed_info


def save_persons(manga, role, persons):
    PeopleRelated: PersonRelatedToManga = manga.people_related.through
    PeopleRelated.objects.filter(role=role).delete()
    PeopleRelated.objects.bulk_create(
        [
            PeopleRelated(
                person=Person.objects.get_or_create(name=person)[INSTANCE],
                manga=manga,
                role=role,
            )
            for person in persons
        ],
        ignore_conflicts=True,
    )


def save_detailed_manga_info(
    manga: Manga,
    authors=None,
    year=None,
    description=None,
    translators=None,
    illustrators=None,
    screenwriters=None,
    categories=None,
    rss_url=None,
) -> None:
    if manga is None:
        return

    manga.year = year
    manga.rss_url = manga.domain + rss_url
    manga.description = description

    save_persons(manga, PersonRelatedToManga.Roles.author, authors)
    save_persons(manga, PersonRelatedToManga.Roles.illustrator, illustrators)
    save_persons(manga, PersonRelatedToManga.Roles.screenwriter, screenwriters)
    save_persons(manga, PersonRelatedToManga.Roles.translator, translators)

    categories = [
        Category.objects.get_or_create(name=category)[INSTANCE] for category in categories
    ]
    manga.categories.clear()
    manga.categories.set(categories)
    manga.updated_detail = dt.datetime.now(pytz.UTC)
    manga.save()


def is_need_update(manga: Manga):
    if manga.updated_detail:
        update_deadline = manga.updated_detail + dt.timedelta(minutes=30)
        if dt.datetime.now(pytz.UTC) >= update_deadline:
            return True
        else:
            logger.info(f"Manga {manga.alt_title} is already up to date")
            return False
    else:
        return True


def deepen_manga_info(id: int) -> Optional[dict]:
    manga = Manga.objects.filter(pk=id).first()
    if manga is None:
        logger.error("Manga not found")
        return

    if not is_need_update(manga):
        return

    url = manga.source_url
    info: dict = get_detailed_info(url)
    save_detailed_manga_info(manga=manga, **info)
    logger.info(f"Successful detailing of manga {manga.alt_title}")
    return info
