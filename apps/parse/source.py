# TODO: add parsing of readmanga's alias sites
# Like change dynamically url or something


CATALOGUES = {
    "readmanga": {
        "source": "https://readmanga.live",
        "settings": "apps.readmanga.settings",
    },
    "mintmanga": {
        "source": "https://mintmanga.live",
        "settings": "apps.readmanga.settings",
    },
    "selfmanga": {
        "source": "https://selfmanga.live",
        "settings": "apps.readmanga.settings",
    },
    "rumix": {
        "source": "https://rumix.me",
        "settings": "apps.readmanga.settings",
    },
    "mangachan": {
        "source": "https://manga-chan.me",
        "settings": "apps.mangachan.settings",
    },
}
CATALOGUE_NAMES = [k.lower() for k in CATALOGUES.keys()]

SOURCE_TO_CATALOGUE_MAP = {CATALOGUES[key]["source"]: key for key in CATALOGUES}
