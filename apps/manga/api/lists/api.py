from typing import List

from django.db import IntegrityError
from django.db.transaction import atomic
from ninja import Router

from apps.core.api.schemas import ErrorSchema
from apps.manga.annotate import fast_annotate_manga_query
from apps.manga.api.lists.schemas import SaveListEditOut, SaveListOut
from apps.manga.models import SaveList, SaveListMangaThrough
from apps.manga.signals import create_save_lists

list_router = Router(tags=["Lists"])


# TODO: better way to query with user/session
# TODO: preserve order with LIST_NAMES and add it to custom queryset
# TODO: stop using django extra?


@list_router.get("/", response=List[SaveListOut])
def get_all_lists(request):
    user_kw = dict(user=request.user)

    if not request.user.is_authenticated:
        if not request.session.session_key:
            request.session.create()
        user_kw = dict(session=request.session.session_key)
        create_save_lists(**user_kw)

    save_lists = SaveList.objects.filter(**user_kw).order_by("id").all()

    return [
        SaveListOut(
            id=save_list.id,
            name=save_list.name,
            mangas=fast_annotate_manga_query(save_list.mangas.all()),
        )
        for save_list in save_lists
    ]


@list_router.post("/{list_id}/{manga_id}/", response=SaveListEditOut)
def add_manga_to_list(request, list_id: int, manga_id: int):
    user_kw = (
        dict(user=request.user)
        if request.user.is_authenticated
        else dict(session=request.session.session_key)
    )

    qs = SaveList.objects.filter(id=list_id, **user_kw)
    if not qs:
        return ErrorSchema(error="List not found.")

    try:
        with atomic():
            nested_user_kw = {f"save_list__{k}": v for k, v in user_kw.items()}
            SaveListMangaThrough.objects.filter(manga_id=manga_id, **nested_user_kw).delete()
            SaveListMangaThrough.objects.create(save_list_id=list_id, manga_id=manga_id)
        return SaveListEditOut(count=1)
    except IntegrityError as e:
        if "already_exists" in str(e):
            return ErrorSchema(error="Record already exists.")
        return ErrorSchema(error=str(e))


@list_router.delete("/{list_id}/{manga_id}/", response=SaveListEditOut)
def remove_manga_from_list(request, list_id: int, manga_id: int):
    user_kw = (
        dict(save_list__user=request.user)
        if request.user.is_authenticated
        else dict(save_list__session=request.session.session_key)
    )

    count, _ = SaveListMangaThrough.objects.filter(
        manga_id=manga_id,
        save_list_id=list_id,
        **user_kw,
    ).delete()
    return SaveListEditOut(count=count)
