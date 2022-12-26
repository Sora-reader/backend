from typing import Optional

from ninja import Schema


class BookmarkOut(Schema):
    chapter_id: Optional[int]


class BookmarkEditOut(Schema):
    count: int
