from django.urls import path

from .views import SignUpView

urlpatterns = [
    path(r"sign-up/", SignUpView.as_view()),
]
