from django.db import IntegrityError
from django.db.transaction import atomic
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from apps.core.api.schemas import ErrorSchema
from apps.manga.api.notifications.schemas import (
    ChapterNotificationEditOut,
    ChapterNotificationList,
    ChapterNotificationOut,
)
from apps.manga.models import ChapterNotification

chapter_notification_router = Router(tags=["ChapterNotifications"], auth=JWTAuth())


@chapter_notification_router.get("/", response=ChapterNotificationList)
def get_chapter_notification(request):
    qs = (
        ChapterNotification.objects.filter(user_id=request.user)
        .values("id", "chapter__title", "chapter__manga__thumbnail", "created")
        .order_by("-id")
    )

    return [
        ChapterNotificationOut(
            id=notification["id"],
            chapter_title=notification["chapter__title"],
            manga_thumbnail=notification["chapter__manga__thumbnail"],
            date_time=notification["created"],
        )
        for notification in qs
    ]


@chapter_notification_router.delete("/{notification_id}/", response=ChapterNotificationEditOut)
def remove_chapter_notification(request, notification_id: int):
    try:
        with atomic():
            ChapterNotification.objects.filter(
                user=request.user, notification_id=notification_id
            ).delete()
        return ChapterNotificationEditOut(count=1)
    except IntegrityError as e:
        return ErrorSchema(error=str(e))
