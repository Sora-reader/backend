import logging
import urllib.request
from http.client import IncompleteRead
from xml.etree import ElementTree

logging.basicConfig(level=logging.ERROR)


def get_readmanga_map() -> str:
    while True:
        try:
            url = "https://readmanga.live/sitemap.xml"
            with urllib.request.urlopen(url) as u:
                return u.read().decode()
        except IncompleteRead:
            logging.error("Getting readmanga map failure: retrying")
            continue


def get_manga_urls():
    schema = get_readmanga_map()

    namespaces = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    et = ElementTree.fromstring(schema)
    root = et
    urls = []
    for child in root.findall("sitemap:url", namespaces):
        for s in child.findall("sitemap:loc", namespaces):
            urls.append(s.text)
    return urls
