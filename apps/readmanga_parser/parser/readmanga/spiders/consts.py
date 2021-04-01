NAME_TAG = '//span[@class = "name"]/text()'
AUTHOR_TAG = '//div[@class = "subject-meta col-sm-7"]/p[@class = "elementList"]/span[@class = "elem_author "] \
            /a[@class = "person-link"]/text()'
YEAR_TAG = '//div[@class = "subject-meta col-sm-7"]/p[@class = "elementList"]/span[@class = "elem_year "] \
            /a[@class = "element-link"]/text()'
TRANSLATORS_TAG = '//div[@class = "subject-meta col-sm-7"]/p[@class = "elementList"]/span[@class = "elem_translator "] \
            /a[@class = "person-link"]/text()'

CHAPTERS_TAG = '//table[@class = "table table-hover"]//a/@href|//table[@class = "table table-hover"]//a/text()'

# descriptors for main manga catalogue

DESCRIPTIONS_DESCRIPTOR = '//div[@class = "tiles row"]//div[contains(@class, "tile col-sm-6")]'

DESC_TEXT_DESCRIPTOR = '//div[@class = "hidden long-description-holder"]//text()'
TITLE_DESCRIPTOR = "//h3/a/@title"
TITLE_URL_DESCRIPTOR = "//h3/a/@href"
GENRES_DESCRIPTOR = '//div[@class = "tile-info"]//a[@class = "element-link"]/text()'
IMG_URL_DESCRIPTOR = '//img[@class = "lazy img-responsive"]/@data-original'
