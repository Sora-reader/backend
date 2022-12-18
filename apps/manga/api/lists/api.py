from typing import List

from django.db import IntegrityError
from django.db.transaction import atomic
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from apps.core.api.schemas import ErrorSchema
from apps.manga.annotate import fast_annotate_manga_query
from apps.manga.api.lists.schemas import SaveListEditOut, SaveListOut
from apps.manga.models import SaveList, SaveListMangaThrough

list_router = Router(tags=["Lists"], auth=JWTAuth())


@list_router.get("/", response=List[SaveListOut])
def get_all_lists(request):
    save_lists = SaveList.objects.filter(user=request.user).order_by("id").all()

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
    qs = SaveList.objects.filter(user=request.user, id=list_id)
    if not qs:
        return ErrorSchema(error="List not found.")

    try:
        with atomic():
            SaveListMangaThrough.objects.filter(
                manga_id=manga_id, save_list__user=request.user
            ).delete()
            SaveListMangaThrough.objects.create(save_list_id=list_id, manga_id=manga_id)
        return SaveListEditOut(count=1)
    except IntegrityError as e:
        if "already_exists" in str(e):
            return ErrorSchema(error="Record already exists.")
        return ErrorSchema(error=str(e))


@list_router.delete("/{list_id}/{manga_id}/", response=SaveListEditOut)
def remove_manga_from_list(request, list_id: int, manga_id: int):
    count, _ = SaveListMangaThrough.objects.filter(
        manga_id=manga_id, save_list_id=list_id, save_list__user=request.user
    ).delete()
    return SaveListEditOut(count=count)
