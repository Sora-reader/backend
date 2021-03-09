from xml.etree import ElementTree
import urllib.request


def get_manga_urls():

    schema = ''
    url = 'https://readmanga.live/sitemap.xml'
    with urllib.request.urlopen(url) as u:
        schema = u.read().decode()

    namespaces = {
        'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
    }

    et = ElementTree.fromstring(schema)
    root = et
    urls = []
    for child in root.findall('sitemap:url', namespaces):
        for s in child.findall('sitemap:loc', namespaces):
            urls.append(s.text)
    return urls
