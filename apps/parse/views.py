from django.db.models.query_utils import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.parse.models import Manga
from apps.parse.serializers import MangaChaptersSerializer, MangaSerializer


class MangaViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MangaSerializer
    queryset = Manga.objects.all()

    def get_object(self):
        return get_object_or_404(Manga, id=self.kwargs.get("pk"))

    @extend_schema(
        parameters=[
            OpenApiParameter("manga_id", OpenApiTypes.NUMBER, OpenApiParameter.PATH),
        ]
    )
    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<manga_id>[^/.]+)/volumes",
    )
    def chapters_list(self, request, manga_id):
        mangas = Manga.objects.filter(id=manga_id)
        serializer = MangaChaptersSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("manga_id", OpenApiTypes.NUMBER, OpenApiParameter.PATH),
            OpenApiParameter("volume_id", OpenApiTypes.NUMBER, OpenApiParameter.PATH),
            OpenApiParameter("chapter_id", OpenApiTypes.NUMBER, OpenApiParameter.PATH),
        ]
    )
    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<manga_id>[^/.]+)/(?P<volume_id>[^/.]+)/(?P<chapter_id>[^/.]+)",
    )
    def images_list(self, request, manga_id, volume_id, chapter_id):
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("title", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ]
    )
    @action(
        detail=False,
        methods=("get",),
        url_path="search",
    )
    def search(self, request):
        title = request.GET.get("title", None)
        if not title:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mangas = Manga.objects.filter(Q(title__icontains=title) | Q(alt_title__icontains=title))
        serializer = MangaSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
