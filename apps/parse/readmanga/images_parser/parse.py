import ast
import re

import requests

COUNT_LINK_ELEMENTS = 3


def find_image(html: str) -> list[str]:
    image_links = []
    image_hints = re.search(r"rm_h.init\( \[(.*)\],.*\)", html)
    if image_hints:
        image_links = [
            "".join(image[:COUNT_LINK_ELEMENTS]) for image in ast.literal_eval(image_hints.group(1))
        ]
    return image_links


def images_manga_info(url: str) -> list[str]:
    response = requests.get(url)

    if not response.ok:
        return []

    html_response = response.text
    return find_image(html_response)
