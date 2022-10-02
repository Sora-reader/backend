from django.contrib import admin
from django.urls import include, path, re_path

from manga_reader.api import api

urlpatterns = [
    path("api/", api.urls),
    path("django-rq/", include("django_rq.urls")),
    re_path(r"^(?!api)\w*?", admin.site.urls),
]
