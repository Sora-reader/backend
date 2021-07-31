from django.db.models.query_utils import Q
from requests.exceptions import MissingSchema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.core.utils import format_error_response, init_redis_client
from apps.parse.models import Chapter, Manga
from apps.parse.readmanga.chapter_parser.parse import chapters_manga_info
from apps.parse.readmanga.detail_parser.parse import deepen_manga_info
from apps.parse.readmanga.images_parser.parse import parse_new_images
from apps.parse.serializers import MangaChaptersSerializer, MangaSerializer
from apps.parse.utils import get_source_url_from_source


class MangaViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MangaSerializer
    queryset = Manga.objects.all()
    redis_client = init_redis_client()

    def retrieve(self, request, pk, *args, **kwargs):
        manga = Manga.objects.filter(pk=pk).first()
        if manga:
            deepen_manga_info(pk)
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<manga_id>[^/.]+)/chapters",
    )
    def chapters_list(self, request, manga_id):
        manga: Manga = get_object_or_404(Manga, id=manga_id)
        try:
            chapters_manga_info(manga.pk)
        except MissingSchema:
            return format_error_response("Parse the manga details first")
        serializer = MangaChaptersSerializer(
            manga.chapters.order_by("-volume", "-number").all(), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<chapter_id>[^/.]+)/images",
    )
    def images_list(self, request, chapter_id):
        chapter: Chapter = get_object_or_404(Chapter, id=chapter_id)
        parse = request.GET.get("parse", None)
        images_cached = self.redis_client.exists(chapter.link)
        if not images_cached or parse is not None:
            return Response(
                parse_new_images(chapter.link, self.redis_client), status=status.HTTP_200_OK
            )
        return Response(self.redis_client.lrange(chapter.link, 0, -1), status=status.HTTP_200_OK)

    @staticmethod
    def get_search_filter(request):
        """Get search query filter"""
        title: str = request.GET.get("title", None)
        catalogue: str = request.GET.get("catalogue", None)

        if not title:
            raise ValueError("No title found")

        search_filter = Q(title__icontains=title) | Q(alt_title__icontains=title)

        if catalogue:
            catalogue_url = get_source_url_from_source(catalogue.capitalize())
            if catalogue_url:
                search_filter = search_filter & Q(source_url__contains=catalogue_url)
            else:
                raise ValueError(f"Catalogue should be one of {', '.join(Manga.SOURCE_MAP.keys())}")

        print(search_filter)

        return search_filter

    @action(
        detail=False,
        methods=("get",),
        url_path="search",
    )
    def search(self, request):
        query_filter = self.get_search_filter(request)
        if not query_filter:
            return format_error_response(query_filter)
        mangas = Manga.objects.filter(query_filter)

        page = self.paginate_queryset(mangas)
        if page is not None:
            serializer = MangaSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MangaSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
