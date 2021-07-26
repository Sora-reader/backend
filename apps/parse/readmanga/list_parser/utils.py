import re


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


def parse_rating(rate_str: str):
    """
    rate_str example '9.439212799072266 из 10'
    """
    try:
        rating = round(float(rate_str.split(" из ")[0]) / 2, 2)
    except Exception:
        rating = 0.0
    return rating
