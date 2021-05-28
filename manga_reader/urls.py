from django.conf.urls import include
from django.contrib import admin
from django.urls import path

apipatterns = [
    path("docs/", include("apps.api_docs.urls")),
    path("readmanga/", include("apps.readmanga_parser.urls")),
    path("auth/", include("apps.login.urls")),
]

urlpatterns = [
    path("api/", include(apipatterns)),
    path("", admin.site.urls),
]
