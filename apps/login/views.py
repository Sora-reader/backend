from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from apps.login.serializers import users


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=users.UserSerializer,
        responses=users.UserTokenResponseSerializer,
    )
    @action(methods=("post",), detail=False, url_path="sign-up")
    def post(self, request, *args, **kwargs):
        user_serializer = users.UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.create(validated_data=user_serializer.validated_data)

        token = user_serializer.get_token()
        token["username"] = user_serializer.validated_data["username"]
        return Response(token, status=status.HTTP_201_CREATED)


class SignInView(TokenViewBase):
    serializer_class = users.UserTokenRequestSerializer

    @extend_schema(
        request=users.UserTokenRequestSerializer,
        responses=users.UserTokenResponseSerializer,
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class SignOutView(APIView):
    @extend_schema(description="Sign user out and blacklist his token")
    def get(self, request):
        print("Blacklisting")
        refresh = request.COOKIES.get("sora_refresh")
        if refresh:
            try:
                print("Blocking token ", refresh)
                token = RefreshToken(refresh)
                token.blacklist()
            except (TokenError, TokenBackendError):
                print("Token already expired")
        else:
            print("No token, nothing to blacklist")
        return HttpResponse(status=200)
