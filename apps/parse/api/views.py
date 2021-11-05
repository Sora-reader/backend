from django.conf import settings
from django.http.response import Http404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.core.fast import FastLimitOffsetPagination
from apps.core.fast.utils import get_fast_response
from apps.core.utils import format_error_response, init_redis_client
from apps.parse.api.serializers import CHAPTER_FIELDS, MANGA_FIELDS
from apps.parse.const import CHAPTER_PARSER, DETAIL_PARSER, IMAGE_PARSER
from apps.parse.documents import MangaDocument
from apps.parse.models import Chapter, Manga
from apps.parse.scrapy.utils import run_parser
from apps.parse.utils import fast_annotate_manga_query, needs_update


class MangaViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = FastLimitOffsetPagination
    queryset = Manga.objects.all()
    redis_client = init_redis_client()

    @classmethod
    def get_fast_manga(cls, pk) -> dict:
        manga = fast_annotate_manga_query(Manga.objects.filter(pk=pk))
        if not manga.exists():
            raise Http404
        return manga.parse_values(*MANGA_FIELDS)[0]

    def retrieve(self, _, pk, *args, **kwargs):
        manga = self.get_fast_manga(pk)
        try:
            if needs_update(manga["updated_detail"]):
                run_parser(DETAIL_PARSER, manga.source, manga["source_url"])
        except Exception as e:
            return format_error_response("Errors occured during parsing" + str(e))
        return get_fast_response(manga)

    def list(self, request):
        title: str = request.GET.get("title", None)
        if not title:
            return format_error_response("No title found")

        mangas = fast_annotate_manga_query(
            MangaDocument.search()
            .query("fuzzy", title=title)[: settings.REST_FRAMEWORK["PAGE_SIZE"]]
            .to_queryset()
        )

        page = self.paginator.paginate_queryset(
            mangas,
            request,
            values=MANGA_FIELDS,
        )
        if page is not None:
            return self.paginator.get_paginated_response(page)

        return Response(list(mangas.parse_values(*MANGA_FIELDS)), status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<pk>[^/.]+)/chapters",
    )
    def chapters_list(self, _, pk):
        manga: Manga = Manga.objects.prefetch_related("chapters").get(pk=pk)

        try:
            if needs_update(manga["updated_detail"]):
                run_parser(DETAIL_PARSER, manga.source, manga["source_url"])
                run_parser(CHAPTER_PARSER, manga.source, manga["source_url"])
        except Exception as e:
            return format_error_response("Errors occured during parsing" + str(e))
        return get_fast_response(
            list(manga.chapters.order_by("-volume", "-number").values(*CHAPTER_FIELDS))
        )

    @action(
        detail=False,
        methods=("get",),
        url_path="(?P<chapter_id>[^/.]+)/images",
    )
    def images_list(self, request, chapter_id):
        chapter: Chapter = get_object_or_404(Chapter, id=chapter_id)
        parse = request.GET.get("parse", None)
        images = self.redis_client.lrange(chapter.link, 0, -1)
        if not images or parse is not None:
            run_parser(IMAGE_PARSER, chapter.manga.source, chapter.link)
        return Response(self.redis_client.lrange(chapter.link, 0, -1), status=status.HTTP_200_OK)
