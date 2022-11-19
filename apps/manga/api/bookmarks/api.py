from django.db import IntegrityError
from django.db.transaction import atomic
from ninja import Router

from apps.core.api.schemas import ErrorSchema
from apps.manga.api.bookmarks.schemas import BookmarkEditOut, BookmarkOut
from apps.manga.models import Bookmark

bookmark_router = Router(tags=["Bookmarks"])


@bookmark_router.get("/{manga_id}/", response=BookmarkOut)
def get_bookmark(request, manga_id: int):
    user_kw = (
        dict(user=request.user)
        if request.user.is_authenticated
        else dict(session=request.session.session_key)
    )

    qs = Bookmark.objects.filter(**user_kw, manga_id=manga_id).values_list("chapter_id").first()

    return BookmarkOut(chapter_id=qs[0] if qs else None)


@bookmark_router.post("/{manga_id}/{chapter_id}/", response=BookmarkEditOut)
def set_bookmarks(request, manga_id: int, chapter_id: int):
    user_kw = (
        dict(user=request.user)
        if request.user.is_authenticated
        else dict(session=request.session.session_key)
    )

    try:
        with atomic():
            Bookmark.objects.update_or_create(
                **user_kw, manga_id=manga_id, defaults={"chapter_id": chapter_id}
            )
        return BookmarkEditOut(count=1)
    except IntegrityError as e:
        return ErrorSchema(error=str(e))


@bookmark_router.delete("/{manga_id}/{chapter_id}/", response=BookmarkEditOut)
def remove_bookmark(request, manga_id: int, chapter_id: int):
    user_kw = (
        dict(user=request.user)
        if request.user.is_authenticated
        else dict(session=request.session.session_key)
    )

    try:
        with atomic():
            Bookmark.objects.filter(**user_kw, manga_id=manga_id, chapter_id=chapter_id).delete()
        return BookmarkEditOut(count=1)
    except IntegrityError as e:
        return ErrorSchema(error=str(e))
