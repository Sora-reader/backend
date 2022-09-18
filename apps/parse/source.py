LIST_PARSER = "list"
DETAIL_PARSER = "detail"
CHAPTER_PARSER = "chapters"
IMAGE_PARSER = "images"
PARSER_TYPES = [LIST_PARSER, DETAIL_PARSER, CHAPTER_PARSER, IMAGE_PARSER]

CATALOGUES = {
    "readmanga": {
        "source": "https://readmanga.live",
        "settings": "apps.readmanga.settings",
    }
}
CATALOGUE_NAMES = [k.lower() for k in CATALOGUES.keys()]

SOURCE_TO_CATALOGUE_MAP = {
    "https://readmanga.live": "readmanga",
}
CATALOGUE_TO_SOURCE_MAP = {v: k for k, v in SOURCE_TO_CATALOGUE_MAP.items()}
