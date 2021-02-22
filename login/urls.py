from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from .views import RegistrationView

urlpatterns = [
    url(r'^auth-jwt/', obtain_jwt_token),
    url(r'^auth-jwt-refresh/', refresh_jwt_token),
    url(r'^auth-jwt-verify/', verify_jwt_token),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'registration/', RegistrationView.as_view())
]
