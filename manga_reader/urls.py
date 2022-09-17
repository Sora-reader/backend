from django.contrib import admin
from django.urls import path, re_path

from manga_reader.api import api

urlpatterns = [
    path("api/", api.urls),
    re_path(r"^(?!api)\w*?", admin.site.urls),
]
