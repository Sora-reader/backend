from django.conf.urls import include
from django.contrib import admin
from django.http import request
from django.http.response import HttpResponse
from django.urls import path
from django.urls.conf import re_path
from django.views.defaults import page_not_found

apipatterns = [
    path("docs/", include("apps.api_docs.urls")),
    path("manga/", include("apps.parse.urls")),
    path("auth/", include("apps.login.urls")),
]

urlpatterns = [
    path("api/", include(apipatterns)),
    path(r"", admin.site.urls),
]
