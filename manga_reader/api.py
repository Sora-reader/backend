from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from apps.manga.api.api import manga_router
from apps.manga.api.bookmarks.api import bookmark_router
from apps.manga.api.lists.api import list_router

api = NinjaExtraAPI(title="Sora API", docs_url="/docs/")
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/manga/", manga_router)
api.add_router("/lists/", list_router)
api.add_router("/bookmarks/", bookmark_router)


@api.get("/health", tags=["Meta"])
def healthcheck(request):
    return {}
