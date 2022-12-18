from datetime import datetime
from typing import List

from ninja import Schema


class ChapterNotificationOut(Schema):
    id: int
    chapter_title: str
    manga_thumbnail: str
    date_time: datetime


ChapterNotificationList = List[ChapterNotificationOut]


class ChapterNotificationEditOut(Schema):
    count: int
