from apps.parse.catalogue import BaseCatalogue


class Mangachan(BaseCatalogue):
    name = "mangachan"
    source = "https://manga-chan.me"
    settings = "apps.mangachan.settings"
