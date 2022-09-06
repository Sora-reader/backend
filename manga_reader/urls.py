from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

from manga_reader.api import api

api_patterns = [
    # path("docs/", include("apps.api_docs.urls")),
    # path("manga/", api.urls),
    # path("auth/", include("apps.login.urls")),
]

urlpatterns = [
    path("api/", api.urls),
    # path("api/", include(api_patterns)),
    re_path(r"^(?!api)\w*?", admin.site.urls),
]
