from django.conf.urls import include
from django.contrib import admin
from django.urls import path

apipatterns = [
    path("auth/", include("login.urls")),
    path("readmanga/", include("readmanga_parser.urls")),
]

urlpatterns = [
    path("", admin.site.urls),
    path("api", include(apipatterns)),
]
