from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .queries import ProfileQueries


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(ObtainAuthToken):

    def __register(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            return ProfileQueries.create(username, password)
        except IntegrityError:
            return HttpResponse("User already exists", status=500)

    def post(self, request, *args, **kwargs):
        self.__register(request)

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })
