from allauth.socialaccount.providers.google.views import oauth2_login
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.authentication.utils import auto_save_frontend_url

urlpatterns = [
    path("oauth/", csrf_exempt(auto_save_frontend_url(oauth2_login))),
]
