from typing import List

from django.db.models import CharField, Q

from apps.core.fast import FastQuerySet
from apps.parse.source import SOURCE_TO_CATALOGUE_MAP


def fast_annotate_manga_query(query: FastQuerySet) -> List[dict]:
    """Use 'fast' module to annotate all required fields for manga"""
    return (
        query.cast(id=CharField())
        .map(source=("source_url__startswith", SOURCE_TO_CATALOGUE_MAP))
        .m2m_agg(
            authors=(
                "person_relations__person__name",
                Q(person_relations__role="author"),
            ),
            screenwriters=(
                "person_relations__person__name",
                Q(person_relations__role="screenwriter"),
            ),
            illustrators=(
                "person_relations__person__name",
                Q(person_relations__role="illustrator"),
            ),
            translators=(
                "person_relations__person__name",
                Q(person_relations__role="translator"),
            ),
            genres="genres__name",
            categories="categories__name",
        )
        .parse_values()
    )
