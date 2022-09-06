import logging

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from apps.login.serializers import users


class SignUpView(APIView):
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

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class SignOutView(APIView):
    def get(self, request):
        logging.info("Blacklisting")
        refresh = request.COOKIES.get("sora_refresh")
        if refresh:
            try:
                logging.info("Blocking token ", refresh)
                token = RefreshToken(refresh)
                token.blacklist()
            except (TokenError, TokenBackendError):
                logging.info("Token already expired")
        else:
            logging.info("No token, nothing to blacklist")
        return HttpResponse(status=200)
