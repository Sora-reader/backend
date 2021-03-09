from xml.etree import ElementTree

et = ElementTree.parse('readmanga/quotes-readmanga.live.xml')
root = et.getroot()


def get_manga_urls():
    urls = []
    for child in root:
        for s in child:
            if s.tag == 'loc':
                urls.append(s.text)
    return urls
