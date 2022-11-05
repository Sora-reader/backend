from enum import StrEnum


class ParserType(StrEnum):
    list = "list"
    detail = "detail"
    chapter = "chapters"
    image = "images"


class CacheType(StrEnum):
    detail = "detail"
    chapter = "chapters"
    image = "images"
