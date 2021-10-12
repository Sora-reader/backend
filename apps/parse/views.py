from django.db.models.query_utils import Q
from django.http.response import Http404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.core.fast import FastLimitOffsetPagination
from apps.core.utils import format_error_response, init_redis_client
from apps.parse.models import Chapter, Manga
from apps.parse.parsers import CHAPTER_PARSER, DETAIL_PARSER, PARSERS
from apps.parse.readmanga.detail_parser.parse import deepen_manga_info
from apps.parse.readmanga.images_parser.parse import parse_new_images
from apps.parse.serializers import MANGA_FIELDS, MangaChaptersSerializer, MangaSerializer
from apps.parse.utils import fast_annotate_manga_query, get_source_url_from_source


class MangaViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MangaSerializer
    pagination_class = FastLimitOffsetPagination
    queryset = Manga.objects.all()
    redis_client = init_redis_client()

    def retrieve(self, request, pk, *args, **kwargs):
        manga = (
            Manga.objects.filter(pk=pk)
            .prefetch_related("genres")
            .prefetch_related("categories")
            .prefetch_related("person_relations")
            .first()
        )
        if not manga:
            raise Http404
        deepen_manga_info(pk)
        serializer = self.get_serializer(manga)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<manga_id>[^/.]+)/chapters",
    )
    def chapters_list(self, request, manga_id):
        manga: Manga = get_object_or_404(Manga, id=manga_id)
        chapter_parser = PARSERS[manga.source][CHAPTER_PARSER]
        detail_parser = PARSERS[manga.source][DETAIL_PARSER]
        try:
            detail_parser(manga.pk)
            chapter_parser(manga.pk)
        except Exception as e:
            return format_error_response("Errors occured during parsing" + str(e))
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

        mangas = fast_annotate_manga_query(Manga.objects.filter(query_filter))

        page = self.paginator.paginate_queryset(
            mangas,
            request,
            values=MANGA_FIELDS,
        )
        if page is not None:
            return self.paginator.get_paginated_response(page)

        serializer = MangaSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
