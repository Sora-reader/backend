from ninja import NinjaAPI

from apps.parse.api.api import router

api = NinjaAPI(title="Sora API", docs_url="/docs/")

api.add_router('/manga/', router)
