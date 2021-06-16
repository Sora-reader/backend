# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.parse.queries import MangaQuery
from apps.parse.serializers import MangaSerializer


class SearchAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        title = kwargs.get("title")
        manga = MangaQuery.get_manga_by_title(title=title)
        manga_serializer = MangaSerializer(manga)

        return Response(manga_serializer.data)
