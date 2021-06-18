from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.readmanga_parser.models import Manga
from apps.readmanga_parser.serializers import MangaChaptersSerializer, MangaSerializer


class MangaViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MangaSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Manga.objects.all()

    def get_object(self):
        return get_object_or_404(Manga, id=self.kwargs.get("pk"))

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        methods=("get",),
        url_path="(?P<manga_id>[^/.]+)/chapters",
    )
    def chapters_list(self, request, manga_id):
        mangas = Manga.objects.filter(id=manga_id)
        serializer = MangaChaptersSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        methods=("get",),
        url_path="(?P<manga_id>[^/.]+)/chapter/(?P<chapter_id>[^/.]+)/images",
    )
    def images_list(self, request, manga_id, chapter_id):
        # logic is not working need to update then
        mangas = Manga.objects.filter(id=manga_id, chapters__id=chapter_id)
        serializer = MangaChaptersSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        methods=("get",),
        url_path="search/?title=(?P<title>[^/.]+)",
    )
    def search(self, request, title):
        if not title:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        mangas = Manga.objects.filter(title__contains=title)
        serializer = MangaSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
