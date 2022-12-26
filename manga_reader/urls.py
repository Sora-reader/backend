from django.contrib import admin
from django.urls import include, path, re_path

from manga_reader.api import api

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    #
    path("api/auth/", include("apps.authentication.urls")),
    path("api/", api.urls),
    #
    path("django-rq/", include("django_rq.urls")),
    path("accounts/", include("allauth.urls")),
    #
    re_path(r"^(?!api)\w*?", admin.site.urls),
]
