from ninja import NinjaAPI

from apps.authentication.api.api import router as auth_router
from apps.manga.api.api import manga_router
from apps.manga.api.bookmarks.api import bookmark_router
from apps.manga.api.lists.api import list_router

api = NinjaAPI(title="Sora API", docs_url="/docs/")

api.add_router("/manga/", manga_router)
api.add_router("/lists/", list_router)
api.add_router("/bookmarks/", bookmark_router)
api.add_router("/auth/", auth_router)


@api.get("/health", tags=["Meta"])
def healthcheck(request):
    return {}
