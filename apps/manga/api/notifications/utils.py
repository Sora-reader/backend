from apps.manga.models import Chapter, ChapterNotification, SaveListMangaThrough


def notify_about_chapter(chapter: Chapter):
    qs = SaveListMangaThrough.objects.filter(manga_id=chapter.manga_id).values_list(
        "save_list__user", flat=True
    )
    for user_to_notify in qs:
        ChapterNotification.objects.create(
            user_id=user_to_notify,
            chapter=chapter,
        )
