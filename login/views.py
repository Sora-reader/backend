from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .queries import ProfileQueries

@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(TokenObtainSlidingView):

    def __get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def __register(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            return ProfileQueries.create(username, password)
        except IntegrityError:
            return HttpResponse({'error': 'User already exists'}, status=500)

    def post(self, request, *args, **kwargs):
        user = self.__register(request)
        token = self.__get_token_for_user(user)

        return Response({
            'token': token['access'],
            'username': user.username,
        }, status=200)
