import datetime as dt
import logging
from typing import Optional

import lxml.html as lh
import pytz
import requests
from dateutil import parser

from apps.readmanga_parser.models import (
    Author,
    Category,
    Illustrator,
    Manga,
    ScreenWriter,
    Translator,
)
from apps.readmanga_parser.parser.readmanga.spiders.consts import (
    AUTHOR_TAG,
    CATEGORY_TAG,
    CHAPTERS_TAG,
    ILLUSTRATOR_TAG,
    SCREENWRITER_TAG,
    TITLE_DESCRIPTOR,
    TRANSLATORS_TAG,
    YEAR_TAG,
)
from apps.readmanga_parser.parser.readmanga.spiders.utils import (
    chapters_into_dict,
    handle_xpath_response,
)

logger = logging.getLogger("Detailed manga parser")


def clean_list_from_garbage_strings(strings: list) -> list:
    li = list(filter(lambda x: not x.startswith((",", " ")), strings))
    return li


def get_detailed_info(url: str) -> dict:
    manga_html = requests.get(url).text
    manga_html = lh.fromstring(manga_html)

    name_to_save_by = manga_html.xpath(TITLE_DESCRIPTOR)[0]

    author = handle_xpath_response(manga_html, AUTHOR_TAG)
    year = handle_xpath_response(manga_html, YEAR_TAG)
    translators = manga_html.xpath(TRANSLATORS_TAG)
    translators = clean_list_from_garbage_strings(translators)

    chapters = manga_html.xpath(CHAPTERS_TAG)
    chapters = chapters_into_dict(chapters)

    categories = manga_html.xpath(CATEGORY_TAG)
    categories = clean_list_from_garbage_strings(categories)

    illustrators = manga_html.xpath(ILLUSTRATOR_TAG)
    illustrators = clean_list_from_garbage_strings(illustrators)

    screenwriters = manga_html.xpath(SCREENWRITER_TAG)
    screenwriters = clean_list_from_garbage_strings(screenwriters)

    detailed_info = {
        "name": name_to_save_by,
        "author": author,
        "year": year,
        "translators": translators,
        "chapters": chapters,
        "illustrators": illustrators,
        "screenwriters": screenwriters,
        "categories": categories,
    }
    return detailed_info


def save_detailed_manga_info(
    name,
    author=None,
    year=None,
    translators=None,
    chapters=None,
    illustrators=None,
    screenwriters=None,
    categories=None,
) -> None:
    manga = Manga.objects.filter(name__icontains=name).first()
    if manga is None:
        return

    manga.year = year
    manga.chapters = chapters

    # FIXME bulk_get_or_create instead of get_or_create
    author, _ = Author.objects.get_or_create(name=author)
    translator, _ = Translator.objects.get_or_create(name=translators[0])
    illustrator, _ = Illustrator.objects.get_or_create(name=illustrators[0])
    screenwriter, _ = ScreenWriter.objects.get_or_create(name=screenwriters[0])
    category, _ = Category.objects.get_or_create(name=categories[0])

    author.mangas.add(manga)
    manga.illustrators.add(illustrator.id)
    manga.screenwriters.add(screenwriter.id)
    manga.translators.add(translator.id)
    manga.categories.add(category.id)

    time_detailed = str(dt.datetime.now(tz=pytz.UTC))
    manga.technical_params.update({"time_detailed": time_detailed})

    manga.save()


def was_manga_updated(manga):
    if detailed := manga.technical_params.get("time_detailed"):
        detailed = parser.parse(detailed, tzinfos=[pytz.UTC])
        update_deadline = detailed - dt.timedelta(minutes=30)
        if dt.datetime.now(pytz.UTC) > update_deadline:
            msg = f"Manga {manga.name} has been already updated 30 mins ago"
            logger.error(msg)
            return True
    return False


def deepen_manga_info(name: str) -> Optional[dict]:
    manga = Manga.objects.filter(name__icontains=name).first()
    if manga is None:
        logger.error("Manga not found")
        return

    # check if it wasnt updated for a while
    url = manga.self_url
    if was_manga_updated(manga):
        return

    info: dict = get_detailed_info(url)
    save_detailed_manga_info(**info)
    logger.info(f"Successful detailing of manga {manga.name}")
    return info
