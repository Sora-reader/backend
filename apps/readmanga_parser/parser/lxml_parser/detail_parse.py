import datetime as dt
import logging

import lxml.html as lh
import pytz
import requests

from apps.readmanga_parser.models import Author, Manga, Translator
from apps.readmanga_parser.parser.readmanga.spiders.consts import (
    AUTHOR_TAG,
    CHAPTERS_TAG,
    NAME_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)
from apps.readmanga_parser.parser.readmanga.spiders.utils import chapters_into_dict, handle_xpath_response

logger = logging.getLogger("Detailed manga parser")


def get_detailed_info(url: str) -> dict:
    manga_html = requests.get(url).text
    manga_html = lh.fromstring(manga_html)

    name_to_save_by = manga_html.xpath(NAME_TAG)[0]

    author = handle_xpath_response(manga_html, AUTHOR_TAG)
    year = handle_xpath_response(manga_html, YEAR_TAG)
    translators = manga_html.xpath(TRANSLATORS_TAG)

    chapters = manga_html.xpath(CHAPTERS_TAG)
    chapters = chapters_into_dict(chapters)

    detailed_info = {
        "name": name_to_save_by,
        "author": author,
        "year": year,
        "translators": translators,
        "chapters": chapters,
    }
    return detailed_info


def save_detailed_manga_info(name, author=None, year=None, translators=None, chapters=None) -> None:
    manga = Manga.objects.filter(name__icontains=name).first()

    manga.year = year
    manga.chapters = chapters

    # FIXME bulk_get_or_create instead of get_or_create
    author, _ = Author.objects.get_or_create(name=author)
    translator, _ = Translator.objects.get_or_create(name=translators[0])

    author.mangas.add(manga)
    manga.translators.add(translator.id)

    time_detailed = str(dt.datetime.now(tz=pytz.UTC))
    manga.technical_params.update({"time_detailed": time_detailed})

    manga.save()
