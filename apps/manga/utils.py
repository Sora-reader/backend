from datetime import datetime

from django.utils import timezone

from apps.manga.models import Manga, Person, PersonRelatedToManga


def needs_update(updated_detail: str):
    updated_detail = datetime.fromisoformat(updated_detail)
    if updated_detail:
        update_deadline = updated_detail + Manga.BASE_UPDATE_FREQUENCY
        if timezone.now() >= update_deadline:
            return True
    return False


def save_persons(manga, role, persons):
    instance = 0
    people_related: PersonRelatedToManga = manga.people_related.through
    people_related.objects.filter(role=role, manga=manga).delete()
    people_related.objects.bulk_create(
        [
            people_related(
                person=Person.objects.get_or_create(name=person)[instance],
                manga=manga,
                role=role,
            )
            for person in persons
        ],
        ignore_conflicts=True,
    )
