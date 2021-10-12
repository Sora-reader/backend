from rest_framework.pagination import LimitOffsetPagination

from apps.core.fast.utils import get_fast_response


class FastLimitOffsetPagination(LimitOffsetPagination):
    """Custom Pagination class to leverage FastQuerySet/orjson capabilities."""

    def paginate_queryset(self, queryset, request, view=None, values=()):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)

        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return queryset[self.offset : self.offset + self.limit].parse_values(*values)

    def get_paginated_response(self, data):
        return get_fast_response(
            {
                "count": self.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
