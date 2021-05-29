from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.login import views

app_name = "auth"

urlpatterns = [
    path("sign-in/", views.SignInView.as_view(), name="sign_in"),
    path("sign-up/", csrf_exempt(views.SignUpView.as_view()), name="sign_up"),
    path("sign-out/", views.SignOutView.as_view(), name="sign_out"),
    path("token-verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
