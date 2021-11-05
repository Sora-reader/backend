import logging
from datetime import datetime

from django.db.models import Q
from django.utils import timezone

from apps.core.fast import FastQuerySet
from apps.parse.const import SOURCE_TO_CATALOGUE_MAP
from apps.parse.models import Manga, Person, PersonRelatedToManga


def fast_annotate_manga_query(query: FastQuerySet) -> FastQuerySet:
    return query.map(source=("source_url__startswith", SOURCE_TO_CATALOGUE_MAP)).m2m_agg(
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


def needs_update(updated_detail: str):
    updated_detail = datetime.fromisoformat(updated_detail)
    if updated_detail:
        update_deadline = updated_detail + Manga.BASE_UPDATE_FREQUENCY
        if timezone.now() >= update_deadline:
            return True
    return False


def save_persons(manga, role, persons):
    INSTANCE = 0
    PeopleRelated: PersonRelatedToManga = manga.people_related.through
    PeopleRelated.objects.filter(role=role, manga=manga).delete()
    PeopleRelated.objects.bulk_create(
        [
            PeopleRelated(
                person=Person.objects.get_or_create(name=person)[INSTANCE],
                manga=manga,
                role=role,
            )
            for person in persons
        ],
        ignore_conflicts=True,
    )


def mute_logger_stdout(logger_name: str, *other_loggers):
    import warnings

    logger_names = [logger_name, *other_loggers]
    for name in logger_names:
        warnings.filterwarnings("ignore", module=name)
        logger = logging.getLogger(name)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False
