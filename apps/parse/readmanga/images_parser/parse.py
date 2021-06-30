import ast
import re
from copy import deepcopy
from typing import List

import requests

from apps.core.utils import init_redis_client
from apps.parse.models import Chapter, Manga

COUNT_LINK_ELEMENTS = 3


def find_images(html: str) -> List[str]:
    image_links = []
    image_hints = re.search(r"rm_h.init\( \[(.*)\],.*\)", html)
    if image_hints:
        image_links = [
            "".join(image[:COUNT_LINK_ELEMENTS]) for image in ast.literal_eval(image_hints.group(1))
        ]
    return image_links


def parse_images(url: str, force=False) -> List[str]:
    redis_client = init_redis_client()
    images = redis_client.lrange(url, 0, -1)
    if not images or force:
        response = requests.get(url)
        if not response.ok:
            return images

        html_response = response.text
        images = find_images(html_response)

        redis_client.delete(url)
        redis_client.lpush(url, *images)
        redis_client.expire(url, Manga.UPDATED_IMAGE_FREQUENCY)

    return images


def images_manga_info(manga: Manga, **kwargs) -> List[str]:
    options = deepcopy(kwargs)
    chapter: Chapter = manga.volumes.get(volume=options.get("vol"), number=options.get("chapter"))
    return parse_images(chapter.link, options.get("force"))
