import re

from apps.parse.readmanga.readmanga.descr_utils import clear_list_description


def extract_description(response, descriptor) -> str:
    desc = response.xpath(descriptor).extract()
    desc = clear_list_description(desc)
    desc = " ".join(desc)
    return desc


def handle_xpath_response(html_lxml, tag: str) -> str:
    try:
        return html_lxml.xpath(tag)[0]
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
