from django.views.generic.base import View
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.login.serializers.users import UserSerializer


class UserSignupViewset(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=("post",), detail=False, url_path="sign-up")
    def sign_up(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=serializer.validated_data)
        token = serializer.get_token()
        token["username"] = serializer.validated_data["username"]
        return Response(token, status=status.HTTP_201_CREATED)


class SignOutView(View):
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
