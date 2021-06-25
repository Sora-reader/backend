# descriptors for main manga catalogue

MANGA_TILE_TAG = '//div[@class = "tiles row"]//div[contains(@class, "tile col-md-6")]'
TITLE_TAG = "//h3/a[1]/@title"
SOURCE_URL_TAG = "//h3/a[1]/@href"
GENRES_TAG = '//div[@class = "tile-info"]//a[@class = "element-link"]/text()'
THUMBNAIL_IMG_URL_TAG = '//img[contains(@class, "lazy")][1]/@data-original'
ALT_TITLE_URL = "//h4[@title]//text()"
