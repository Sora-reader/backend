from datetime import datetime
from typing import Dict, Tuple, Union

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.expressions import Case, Value, When
from django.db.models.fields import TextField
from django.db.models.query import QuerySet
from typing_extensions import Annotated

from apps.core.abc.models import BaseModel


class FastQuerySet(QuerySet):
    """
    QuerySet with additional map/m2m_agg/parse_values methods.

    Helps to get rid of unnecessary ORM/Serializer stuff and speed up queries
    """

    model: BaseModel

    TYPE_MAP: Annotated[dict, "Mapping to convert DB returned types into JSON-valid types"] = {
        datetime: str,
    }

    def mangle_annotation(self, field: str) -> str:
        """Mangle annotation if needed name to not coflict with any of model's fields."""
        return f"_fast_{field}"

    @classmethod
    def demangle_annotation(cls, field: str) -> str:
        """Mangle annotation if needed name to not coflict with any of model's fields."""
        return field.split("_fast_")[-1]

    def m2m_agg(self, **kwargs: Dict[str, Tuple[str, dict]]):
        """
        Annotate M2Ms with distinct ArrayAgg for a specified field.

        Accept kwargs with value of:
            1. Field string, like 'field__nested_field'
            2. A tuple of field string and a Expression filter, like ('field', Q(field='string'))
        """
        annotation = {}
        for field, args in kwargs.items():
            output = None
            if type(args) is tuple:
                output = ArrayAgg(args[0], filter=args[1], distinct=True)
            else:
                output = ArrayAgg(args, distinct=True)
            annotation[self.mangle_annotation(field)] = output

        return self.annotate(**annotation)

    def map(self, **kwargs: Dict[str, Tuple[str, dict]]):
        """
        Annotate queryset with CASE...WHEN generated to map provided field with python dict.

        Example: some_queryset.map(source=("source_url__startswith", Manga.SOURCE_MAP))
        """
        return self.annotate(
            **{
                self.mangle_annotation(field): Case(
                    *[When(**{clause: k, "then": Value(v)}) for k, v in dictionary.items()],
                    output_field=TextField(),
                )
                for field, (clause, dictionary) in kwargs.items()
            }
        )

    def parse_values(self, *args) -> Union[dict, list]:
        """
        Get queryset's .values(...) and revert mangled annotation names.

        Required if you used .map/.m2m_agg
        """
        result = []
        annotations = self.query.annotations.keys()
        values = map(
            lambda v: self.mangle_annotation(v) if self.mangle_annotation(v) in annotations else v,
            args,
        )

        for item in self.values(*values):
            parsed = {}
            for k, v in item.items():
                convert = self.__class__.TYPE_MAP.get(type(v))

                parsed[self.demangle_annotation(k)] = v if not convert else convert(v)
            result.append(parsed)
        return result
