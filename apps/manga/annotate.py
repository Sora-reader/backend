from typing import List

from django.db.models import CharField, Q

from apps.core.fast import FastQuerySet
from apps.manga.models import Manga
from apps.parse.catalogue import Catalogue


def fast_annotate_manga_query(query: FastQuerySet) -> List[dict]:
    """Use 'fast' module to annotate all required fields for manga"""
    return (
        query.cast(id=CharField())
        .map(source=("source_url__startswith", Catalogue.map.source_to_name_map))
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


def manga_to_annotated_dict(obj: Manga) -> dict:
    return fast_annotate_manga_query(Manga.objects.filter(pk=obj.pk))[0]
