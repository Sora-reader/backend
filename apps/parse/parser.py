from apps.mangachan.detail import MangachanDetailSpider
from apps.mangachan.list import MangachanListSpider
from apps.readmanga.chapter import ReadmangaChapterSpider
from apps.readmanga.detail import ReadmangaDetailSpider
from apps.readmanga.images import ReadmangaImageSpider
from apps.readmanga.list import ReadmangaListSpider

LIST_PARSER = "list"
DETAIL_PARSER = "detail"
CHAPTER_PARSER = "chapters"
IMAGE_PARSER = "images"
PARSER_TYPES = [LIST_PARSER, DETAIL_PARSER, CHAPTER_PARSER, IMAGE_PARSER]

PARSERS = {
    "readmanga": {
        LIST_PARSER: ReadmangaListSpider,
        DETAIL_PARSER: ReadmangaDetailSpider,
        CHAPTER_PARSER: ReadmangaChapterSpider,
        IMAGE_PARSER: ReadmangaImageSpider,
    },
    "mangachan": {
        LIST_PARSER: (MangachanListSpider, None),
        DETAIL_PARSER: (MangachanDetailSpider, 10),
    },
}

DETAIL_CACHE = DETAIL_PARSER
CHAPTER_CACHE = CHAPTER_PARSER
IMAGE_CACHE = IMAGE_PARSER
CACHES = {
    DETAIL_PARSER: DETAIL_CACHE,
    CHAPTER_PARSER: CHAPTER_CACHE,
    IMAGE_PARSER: IMAGE_CACHE,
}
