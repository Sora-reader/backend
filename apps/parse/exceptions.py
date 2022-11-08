from apps.core.api.schemas import ErrorSchema


class NotFound(Exception):
    pass


class CatalogueNotFound(NotFound):
    pass


class ParserNotFound(NotFound):
    pass


class ParsingError(Exception):
    """Any error that may occur during parsing"""


def to_error_schema(error: str | ParsingError) -> ErrorSchema:
    return ErrorSchema(error=str(error))
