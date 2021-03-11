# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from readmanga_parser.queries import MangaQuery
from rest_framework.response import Response
from django.core import serializers


class SearchAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        title = kwargs.get('title')
        manga = MangaQuery().get_manga_by_title(title=title)

        genres = serializers.serialize('json', manga.genres.all())
        categories = serializers.serialize('json', manga.categories.all())
        translators = serializers.serialize('json', manga.translators.all())

        contents = {
            'title': manga.title,
            'description': manga.description,
            'year': manga.year,
            'genres': genres,
            'categories': categories,
            'author': manga.author.name,
            'translators': translators,
        }
        return Response(contents)
