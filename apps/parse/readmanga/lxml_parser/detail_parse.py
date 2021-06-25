import datetime as dt
import logging
from typing import Optional

import lxml.html as lh
import pytz
import requests

from apps.parse.models import Category, Manga, Person, PersonRelatedToManga
from apps.parse.readmanga.readmanga.spiders.consts import (
    AUTHOR_TAG,
    CATEGORY_TAG,
    DESCRIPTION_TAG,
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

    year = handle_xpath_response(manga_html, YEAR_TAG)
    description = handle_xpath_response(manga_html, DESCRIPTION_TAG)
    rss_url = handle_xpath_response(manga_html, RSS_TAG)

    authors = manga_html.xpath(AUTHOR_TAG)
    authors = clean_list_from_garbage_strings(authors)

    translators = manga_html.xpath(TRANSLATORS_TAG)
    translators = clean_list_from_garbage_strings(translators)

    categories = manga_html.xpath(CATEGORY_TAG)
    categories = clean_list_from_garbage_strings(categories)

    illustrators = manga_html.xpath(ILLUSTRATOR_TAG)
    illustrators = clean_list_from_garbage_strings(illustrators)

    screenwriters = manga_html.xpath(SCREENWRITER_TAG)
    screenwriters = clean_list_from_garbage_strings(screenwriters)

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
    INSTANCE = 0
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
    manga.rss_url = rss_url
    manga.description = description

    save_persons(manga, PersonRelatedToManga.Roles.author, authors)
    save_persons(manga, PersonRelatedToManga.Roles.illustrator, illustrators)
    save_persons(manga, PersonRelatedToManga.Roles.screenwriter, screenwriters)
    save_persons(manga, PersonRelatedToManga.Roles.translator, translators)

    categories = [Category.objects.get_or_create(name=category)[0] for category in categories]
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
