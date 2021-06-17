from django.urls import path

from apps.parse.views import SearchAPIView

urlpatterns = [
    path("search/<str:title>", SearchAPIView.as_view()),
]
