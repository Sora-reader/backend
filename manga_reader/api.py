from ninja import NinjaAPI

from apps.manga.api.api import router

api = NinjaAPI(title="Sora API", docs_url="/docs/")

api.add_router("/manga/", router)


@api.get("/health", tags=["Meta"])
def healthcheck(request):
    return {}
