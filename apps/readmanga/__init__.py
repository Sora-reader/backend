from apps.parse.catalogue import BaseCatalogue


class Readmanga(BaseCatalogue):
    name = "readmanga"
    source = "https://readmanga.live"
    settings = "apps.readmanga.settings"
