from django.utils import timezone

from apps.parse.models import Manga, Person, PersonRelatedToManga


def needs_update(manga: Manga, field: str):
    updated_field = getattr(manga, field)
    if updated_field:
        update_deadline = updated_field + Manga.UPDATED_DETAIL_FREQUENCY
        if not timezone.now() >= update_deadline:
            return False
    return True


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
