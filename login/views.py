from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainSlidingView

from .queries import ProfileQueries


@method_decorator(csrf_exempt, name="dispatch")
class RegistrationView(TokenObtainSlidingView):
    @staticmethod
    def get_token_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def register(request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            return ProfileQueries.create(username, password)
        except IntegrityError:
            return HttpResponse({"error": "User already exists"}, status=500)

    def post(self, request, *args, **kwargs):
        user = self.register(request)
        token = self.get_token_for_user(user)

        return Response(
            {
                "token": token["access"],
                "username": user.username,
            },
            status=200,
        )
