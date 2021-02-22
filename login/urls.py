from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import RegistrationView

urlpatterns = [
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'sign-up/', RegistrationView.as_view())
]
