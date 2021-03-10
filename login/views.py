from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Profile
from .queries import ProfileQueries


@method_decorator(csrf_exempt, name="dispatch")
class SignUpView(TokenObtainPairView):
    @staticmethod
    def get_token_for_user(user: Profile) -> dict:
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def register(request) -> Profile:
        username = request.POST.get("username")
        password = request.POST.get("password")
        return ProfileQueries.create(username, password)

    def post(self, request, *args, **kwargs):
        try:
            # If user exists
            if Profile.objects.filter(username=request.username).exists():
                return Response(
                    {
                        "error": "User already exists",
                    },
                    status=400,
                )

            # Then register
            user = self.register(request)
            token = self.get_token_for_user(user)

            return Response(
                {
                    **token,
                    "username": user.username,
                },
                status=200,
            )
        except (IntegrityError, AttributeError, KeyError) as e:
            # On an exception return 500
            return HttpResponse({"error": str(e)}, status=500)
