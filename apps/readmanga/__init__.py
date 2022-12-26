from apps.parse.catalogue import Catalogue


class Readmanga(Catalogue):
    name = "readmanga"
    source = "https://readmanga.live"
    settings = "apps.readmanga.settings"


# TODO: create multi-catalogue or port this with inheritance or something
# "mintmanga": {
#     "source": "https://mintmanga.live",
#     "settings": "apps.readmanga.settings",
# },
# "selfmanga": {
#     "source": "https://selfmanga.live",
#     "settings": "apps.readmanga.settings",
# },
# "rumix": {
#     "source": "https://rumix.me",
#     "settings": "apps.readmanga.settings",
# }
