from django.urls import path

from .views import RegistrationView

urlpatterns = [
    path(r"sign-up/", RegistrationView.as_view()),
]
