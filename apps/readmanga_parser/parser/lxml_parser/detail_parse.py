import logging

import lxml.html as lh
import requests

from apps.readmanga_parser.parser.readmanga.spiders.consts import (
    AUTHOR_TAG,
    CHAPTERS_TAG,
    NAME_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)

logger = logging.getLogger("Detailed manga parser")


def get_detailed_info(url: str) -> dict:
    manga_html = requests.get(url).text
    manga_html = lh.fromstring(manga_html)

    name_to_save_by = manga_html.xpath(NAME_TAG)

    author = manga_html.xpath(AUTHOR_TAG)
    year = manga_html.xpath(YEAR_TAG)
    translators = manga_html.xpath(TRANSLATORS_TAG)
    chapters = manga_html.xpath(CHAPTERS_TAG)

    detailed_info = {
        "name": name_to_save_by,
        "author": author,
        "year": year,
        "translators": translators,
        "chapters": chapters,
    }
    return detailed_info


# TODO
# def save_parsed(**kwargs) -> None:
#     try:
#         name = kwargs['name']
#     except KeyError:
#         logger.critical('Unable to save - name not specified')

#     author = kwargs.get('author')
#     year = kwargs.get('year')
#     translators = kwargs.get('translators')
#     chapters = kwargs.get('chapters')
