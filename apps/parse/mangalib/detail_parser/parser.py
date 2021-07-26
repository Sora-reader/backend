import asyncio
from copy import deepcopy
from typing import Optional

from django.utils import timezone
from pyppeteer import launch
from scrapy.http import HtmlResponse

from apps.parse.models import Category, Genre, Manga, PersonRelatedToManga
from apps.parse.utils import needs_update, save_persons

from .consts import (
    ALT_TAG,
    AUTHORS_TAG,
    CATEGORIES_TAG,
    DESCRIPTION_TAG,
    GENRES_TAG,
    ILLUSTRATORS_TAG,
    RATING_TAG,
    TRANSLATORS_TAG,
    YEAR_TAG,
)


async def get_detailed_info(url: str) -> dict:
    browser = await launch({"headless": True, "args": ["--no-sandbox", "--disable-setuid-sandbox"]})
    page = await browser.newPage()
    await page.setJavaScriptEnabled(False)
    await page.goto(url, {"timeout": 0})
    body = await page.content()
    html_tree = HtmlResponse(url="", body=body, encoding="utf-8")

    alt_title = html_tree.xpath(ALT_TAG).extract_first("")
    year = html_tree.xpath(YEAR_TAG).extract_first("")
    genres = html_tree.xpath(GENRES_TAG).extract()
    description = html_tree.xpath(DESCRIPTION_TAG).extract_first("")
    rating = html_tree.xpath(RATING_TAG).extract_first(0)
    categories = html_tree.xpath(CATEGORIES_TAG).extract()
    authors = html_tree.xpath(AUTHORS_TAG).extract()
    illustrators = html_tree.xpath(ILLUSTRATORS_TAG).extract()
    translators = html_tree.xpath(TRANSLATORS_TAG).extract()

    await browser.close()

    return {
        "alt_title": alt_title,
        "year": year,
        "genres": genres,
        "description": description,
        "rating": rating,
        "categories": categories,
        "authors": authors,
        "illustrators": illustrators,
        "translators": translators,
    }


def save_detailed_manga_info(
    manga: Manga,
    **kwargs,
) -> None:
    INSTANCE = 0
    if manga is None:
        return

    data = deepcopy(kwargs)

    genres = data.pop("genres", [])
    categories = data.pop("categories", [])
    authors = data.pop("authors", [])
    illustrators = data.pop("illustrators", [])
    translators = data.pop("translators", [])

    save_persons(manga, PersonRelatedToManga.Roles.author, authors)
    save_persons(manga, PersonRelatedToManga.Roles.illustrator, illustrators)
    save_persons(manga, PersonRelatedToManga.Roles.translator, translators)

    categories = [
        Category.objects.get_or_create(name=category)[INSTANCE] for category in categories
    ]
    genres = [Genre.objects.get_or_create(name=genre)[INSTANCE] for genre in genres]

    manga.categories.clear()
    manga.categories.set(categories)

    manga.genres.clear()
    manga.genres.set(genres)

    data["updated_detail"] = timezone.now()
    Manga.objects.filter(pk=manga.pk).update(**data)


def detail_manga_parser(id: int) -> Optional[dict]:
    manga = Manga.objects.get(pk=id)

    if needs_update(manga):
        url = f"{manga.source_url}?section=info"
        info: dict = asyncio.get_event_loop().run_until_complete(get_detailed_info(url))
        save_detailed_manga_info(manga=manga, **info)
        return info
