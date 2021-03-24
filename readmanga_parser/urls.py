from django.urls import path

from readmanga_parser.views import SearchAPIView

urlpatterns = [
    path("search/<str:title>", SearchAPIView.as_view()),
]
