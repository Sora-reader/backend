import datetime as dt
import logging
from typing import Optional

import lxml.html as lh
import pytz
import requests

from apps.parse.models import Author, Category, Manga, Person, PersonRole
from apps.parse.readmanga.readmanga.spiders.consts import (  # CHAPTERS_TAG,
    AUTHOR_TAG,
    CATEGORY_TAG,
    ILLUSTRATOR_TAG,
    RSS_TAG,
    SCREENWRITER_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)
from apps.parse.readmanga.readmanga.spiders.utils import handle_xpath_response

logger = logging.getLogger("Detailed manga parser")


def clean_list_from_garbage_strings(strings: list) -> list:
    li = list(filter(lambda x: not x.startswith((",", " ")), strings))
    return li


def get_detailed_info(url: str) -> dict:
    manga_html = requests.get(url).text
    manga_html = lh.fromstring(manga_html)

    author = handle_xpath_response(manga_html, AUTHOR_TAG)

    year = handle_xpath_response(manga_html, YEAR_TAG)

    rss_url = handle_xpath_response(manga_html, RSS_TAG)

    translators = manga_html.xpath(TRANSLATORS_TAG)
    translators = clean_list_from_garbage_strings(translators)

    categories = manga_html.xpath(CATEGORY_TAG)
    categories = clean_list_from_garbage_strings(categories)

    illustrators = manga_html.xpath(ILLUSTRATOR_TAG)
    illustrators = clean_list_from_garbage_strings(illustrators)

    screenwriters = manga_html.xpath(SCREENWRITER_TAG)
    screenwriters = clean_list_from_garbage_strings(screenwriters)

    detailed_info = {
        "author": author,
        "year": year,
        "translators": translators,
        "illustrators": illustrators,
        "screenwriters": screenwriters,
        "categories": categories,
        "rss_url": rss_url,
    }
    return detailed_info


def save_detailed_manga_info(
    manga,
    author=None,
    year=None,
    translators=None,
    illustrators=None,
    screenwriters=None,
    categories=None,
    rss_url=None,
) -> None:
    if manga is None:
        return

    INSTANCE = 0

    manga.year = year
    manga.author = Author.objects.get_or_create(name=author)[INSTANCE]

    translators = PersonRole.objects.bulk_create(
        [
            PersonRole(
                person_role=PersonRole.PersonRoles.TRANSLATOR,
                person=Person.objects.get_or_create(name=translator)[INSTANCE],
                manga=manga,
            )
            for translator in translators
        ],
        ignore_conflicts=True,
    )
    illustrators = PersonRole.objects.bulk_create(
        [
            PersonRole(
                person_role=PersonRole.PersonRoles.ILLUSTRATOR,
                person=Person.objects.get_or_create(name=illustrator)[INSTANCE],
                manga=manga,
            )
            for illustrator in illustrators
        ],
        ignore_conflicts=True,
    )
    screenwriters = PersonRole.objects.bulk_create(
        [
            PersonRole(
                person_role=PersonRole.PersonRoles.SCREENWRITER,
                person=Person.objects.get_or_create(name=screenwriter)[INSTANCE],
                manga=manga,
            )
            for screenwriter in screenwriters
        ],
        ignore_conflicts=True,
    )
    categories = Category.objects.bulk_create(
        [Category(name=category) for category in categories], ignore_conflicts=True
    )

    manga.categories.set(categories)
    manga.rss_url = rss_url
    manga.updated_detail = dt.datetime.now(pytz.UTC)
    manga.save()


def is_need_update(manga: Manga):
    if manga.updated_detail:
        update_deadline = manga.updated_detail - dt.timedelta(minutes=30)
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

    url = manga.self_url
    info: dict = get_detailed_info(url)
    save_detailed_manga_info(manga=manga, **info)
    logger.info(f"Successful detailing of manga {manga.alt_title}")
    return info
