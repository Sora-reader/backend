from django.conf.urls import include
from django.contrib import admin
from django.urls import path

apipatterns = [
    path("docs/", include("apps.api_docs.urls")),
    path("auth/", include("apps.login.urls")),
    path("", include("apps.parse.urls")),
]

urlpatterns = [
    path("api/", include(apipatterns)),
    path("", admin.site.urls),
]
