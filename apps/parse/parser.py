from apps.parse.readmanga.chapter import ReadmangaChapterSpider
from apps.parse.readmanga.detail import ReadmangaDetailSpider
from apps.parse.readmanga.images import ReadmangaImageSpider
from apps.parse.readmanga.list import ReadmangaListSpider

LIST_PARSER = "list"
DETAIL_PARSER = "detail"
CHAPTER_PARSER = "chapters"
IMAGE_PARSER = "images"
PARSER_TYPES = [LIST_PARSER, DETAIL_PARSER, CHAPTER_PARSER, IMAGE_PARSER]

PARSERS = {
    "readmanga": {
        LIST_PARSER: (ReadmangaListSpider, None),
        DETAIL_PARSER: (ReadmangaDetailSpider, 10),
        CHAPTER_PARSER: (ReadmangaChapterSpider, 10),
        IMAGE_PARSER: (ReadmangaImageSpider, 10),
    }
}
