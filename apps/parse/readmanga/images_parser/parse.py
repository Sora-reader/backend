import re
from typing import List

import requests
import ujson
from django.conf import settings

from apps.core.utils import init_redis_client
from apps.parse.models import Chapter, Manga

COUNT_LINK_ELEMENTS = 3


def find_images(html: str) -> List[str]:
    image_links = []
    image_hints = re.search(r"rm_h.initReader\(.*(\[{2}.*\]{2}).*\)", html)
    if image_hints:
        image_links = [
            "".join(image[:COUNT_LINK_ELEMENTS])
            for image in ujson.loads(image_hints.group(1).replace("'", '"'))
        ]
    return image_links


def parse_new_images(url: str, redis_client) -> List[str]:
    images = []
    response = requests.get(url, headers=settings.HEADERS)
    if not response.ok:
        return images

    html_response = response.text
    images = find_images(html_response)

    redis_client.delete(url)
    if images:
        redis_client.rpush(url, *images)
    redis_client.expire(url, Manga.IMAGE_UPDATE_FREQUENCY)

    return images


def parse_images(url: str) -> List[str]:
    redis_client = init_redis_client()
    images = redis_client.lrange(url, 0, -1)
    if not images:
        images = parse_new_images(url, redis_client)
    return images


def images_manga_info(chapter: Chapter) -> List[str]:
    return parse_images(chapter.link)
