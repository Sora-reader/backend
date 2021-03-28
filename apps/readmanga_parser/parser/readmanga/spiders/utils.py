import re

from apps.readmanga_parser.parser.readmanga.descr_utils import clear_list_description


def extract_description(response, descriptor) -> str:
    desc = handle_xpath_response(response, descriptor)
    desc = clear_list_description(desc)
    desc = " ".join(desc)
    return desc


def handle_xpath_response(response, tag: str) -> str:
    try:
        return response.xpath(tag).extract()
    except IndexError:
        return ""


def chapters_into_dict(chapters: list) -> dict:
    regex = "[\n]+|[ ]{2,}"
    chapters = [re.sub(regex, "", chapter) for chapter in chapters]
    readmanga_base_url = "https://readmanga.live"
    links = filter(lambda m: m.startswith("/"), chapters)
    names = filter(lambda n: not n.startswith("/"), chapters)

    chapters_catalogue = {}
    for link, name in zip(links, names):
        chapters_catalogue.update({readmanga_base_url + link: name})

    return chapters_catalogue
