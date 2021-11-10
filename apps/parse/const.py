from datetime import timedelta

from apps.parse.readmanga.chapter import ReadmangaChapterSpider
from apps.parse.readmanga.detail import ReadmangaDetailSpider
from apps.parse.readmanga.images import ReadmangaImageSpider
from apps.parse.readmanga.list import ReadmangaListSpider

BASE_UPDATE_FREQUENCY = timedelta(hours=1)
IMAGE_UPDATE_FREQUENCY = timedelta(hours=8)

LIST_PARSER = "list"
DETAIL_PARSER = "detail"
CHAPTER_PARSER = "chapters"
IMAGE_PARSER = "images"
PARSER_TYPES = [LIST_PARSER, DETAIL_PARSER, CHAPTER_PARSER, IMAGE_PARSER]

CATALOGUES = {
    "readmanga": {
        "source": "https://readmanga.io",
        "settings": "apps.parse.readmanga.settings",
        "parsers": {
            LIST_PARSER: ReadmangaListSpider,
            DETAIL_PARSER: ReadmangaDetailSpider,
            CHAPTER_PARSER: ReadmangaChapterSpider,
            IMAGE_PARSER: ReadmangaImageSpider,
        },
    }
}
CATALOGUE_NAMES = [k.lower() for k in CATALOGUES.keys()]

SOURCE_TO_CATALOGUE_MAP = {
    "https://readmanga.io": "readmanga",
}
CATALOGUE_TO_SOURCE_MAP = {v: k for k, v in SOURCE_TO_CATALOGUE_MAP.items()}
