from enum import Enum


class ParsingStatus(str, Enum):
    """Parsing status ENUM."""

    parsing = "parsing"
    up_to_date = "upToDate"


# Scraped data type
ParsingResult = dict | list

# Possible cache values. Either the status of the data itself
ParsingCacheValue = ParsingStatus | ParsingResult
