from enum import Enum


class ParserType(str, Enum):
    list = "list"
    detail = "detail"
    chapter = "chapter"
    image = "image"


class CacheType(str, Enum):
    detail = "detail"
    chapter = "chapter"
    image = "image"

    @classmethod
    def from_parser_type(cls, type_: str | ParserType) -> str:
        return getattr(cls, type_)


class ParsingStatus(str, Enum):
    """Parsing status ENUM."""

    parsing = "parsing"
    up_to_date = "upToDate"


# Scraped data type
ParsingResult = dict | list

# Possible cache values. Either the status of the data itself
ParsingCacheValue = ParsingStatus | ParsingResult
