from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

apipatterns = [
    path("docs/", include("apps.api_docs.urls")),
    path("manga/", include("apps.parse.api.urls")),
    path("auth/", include("apps.login.urls")),
]

urlpatterns = [
    path("api/", include(apipatterns)),
    re_path(r"^(?!api)\w*?", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
