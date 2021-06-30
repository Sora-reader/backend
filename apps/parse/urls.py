from django.urls import include, path
from rest_framework import routers

from apps.parse.views import MangaViewSet

router = routers.DefaultRouter()

router.register(r"", MangaViewSet, basename="manga")

urlpatterns = [
    path(r"", include(router.urls)),
]
