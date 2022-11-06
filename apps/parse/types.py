from enum import StrEnum


class ParserType(StrEnum):
    list = "list"
    detail = "detail"
    chapter = "chapter"
    image = "image"


class CacheType(StrEnum):
    detail = "detail"
    chapter = "chapter"
    image = "image"

    @classmethod
    def from_parser_type(cls, type_: str | ParserType) -> str:
        return getattr(cls, type_)


class ParsingStatus(StrEnum):
    """Parsing status ENUM."""

    parsing = "parsing"
    up_to_date = "upToDate"


# Scraped data type
ParsingResult = dict | list

# Possible cache values. Either the status of the data itself
ParsingCacheValue = ParsingStatus | ParsingResult
