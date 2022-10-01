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
