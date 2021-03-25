from django.urls import path

from .views import SignUpView

urlpatterns = [
    path("sign-up/", SignUpView.as_view()),
    path("auth/", SignUpView.as_view()),
    path("refresh/", SignUpView.as_view()),
]
