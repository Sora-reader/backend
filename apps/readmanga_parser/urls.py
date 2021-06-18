from django.urls import include, path
from rest_framework import routers

from apps.readmanga_parser.views import MangaViewSet

router = routers.DefaultRouter()

router.register(r"manga", MangaViewSet, basename="manga")

urlpatterns = [
    path(
        r"",
        include(
            router.urls,
        ),
    ),
]
