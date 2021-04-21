from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.login.views import SignOutView, UserSignupViewset

app_name = "auth"

router = DefaultRouter()
router.register("", viewset=UserSignupViewset, basename="sign_up")

urlpatterns = [
    path("", include(router.urls)),
    path("sign-in/", TokenObtainPairView.as_view(), name="sign_in"),
    path("sign-out/", SignOutView.as_view(), name="sign_out"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
