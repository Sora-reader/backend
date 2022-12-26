from datetime import datetime
from decimal import Decimal
from typing import Tuple, Union

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.expressions import Case, Value, When
from django.db.models.fields import TextField
from django.db.models.functions import Cast
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from typing_extensions import Annotated

from apps.core.abc.models import BaseModel


class FastQuerySet(QuerySet):
    """
    QuerySet with additional map/m2m_agg/parse_values methods.

    Helps to get rid of unnecessary ORM/Serializer stuff and speed up queries
    """

    model: BaseModel
    mangle_prefix = "_fast_"

    TYPE_MAP: Annotated[dict, "Mapping to convert DB returned types into JSON-valid types"] = {
        datetime: str,
        # Help orjson a bit
        Decimal: float,
    }

    @classmethod
    def mangle_annotation(cls, field: str) -> str:
        """Mangle annotation if needed name to not conflict with any of model's fields."""
        return cls.mangle_prefix + field

    @classmethod
    def demangle_annotation(cls, field: str) -> str:
        """Reverse field mangling."""
        return field.split(cls.mangle_prefix)[-1]

    def cast(self, **kwargs):
        """
        Simply cast values to a type.

        Example: qs.cast(id=CharField()) will result in {"id": "123", ...}
        """
        return self.annotate(
            **{
                self.mangle_annotation(field): Cast(field, output_field=TextField())
                for field, output_field in kwargs.items()
            }
        )

    def m2m_agg(self, **kwargs: str | Tuple[str, Q]):
        """
        Annotate M2Ms with distinct ArrayAgg for a specified field.

        Accept kwargs with value of:
            1. Field string, like 'field__nested_field'
            2. A tuple of field string and an Expression filter, like ('field', Q(field='string'))
        """
        annotation = {}
        for field, args in kwargs.items():
            if type(args) is tuple:
                output = ArrayAgg(args[0], filter=args[1], distinct=True)
            else:
                output = ArrayAgg(
                    args,
                    # Avoid [null] arrays when using ArrayAgg
                    filter=Q(**{f"{args}__isnull": False}),
                    distinct=True,
                )
            annotation[self.mangle_annotation(field)] = output

        return self.annotate(**annotation)

    def map(self, **kwargs: Tuple[str, dict]):
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
            lambda field: self.mangle_annotation(field)
            if self.mangle_annotation(field) in annotations
            else field,
            args,
        )

        for item in self.values(*values):
            parsed = {}
            for k, v in item.items():
                convert = self.__class__.TYPE_MAP.get(type(v))

                parsed[self.demangle_annotation(k)] = v if not convert else convert(v)
            result.append(parsed)
        return result
