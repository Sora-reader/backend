# descriptors for detail manga parser

RSS_TAG = "//head/link[@type='application/rss+xml']/@href"
AUTHOR_TAG = "//span[@class='elem_author ']/a[@class='person-link']/text()"
YEAR_TAG = "//span[@class='elem_year ']/a[@class='element-link']/text()"
TRANSLATORS_TAG = "//span[@class='elem_translator ']/a[@class='person-link']/text()"
ILLUSTRATOR_TAG = '//span[@class = "elem_illustrator "]/a[@class="person-link"]/text()'
SCREENWRITER_TAG = '//span[@class="elem_screenwriter "]/a[@class="person-link"]/text()'
CATEGORY_TAG = '//span[@class = "elem_category "]/a[@class="element-link"]/text()'

CHAPTERS_TAG = (
    '//table[@class = "table table-hover"]//a/@href|//table[@class = "table table-hover"]//a/text()'
)

# descriptors for main manga catalogue

DESCRIPTIONS_DESCRIPTOR = '//div[@class = "tiles row"]//div[contains(@class, "tile col-md-6")]'

DESC_TEXT_DESCRIPTOR = '//div[@class = "hidden long-description"]//text()'
TITLE_DESCRIPTOR = "//h3/a/@title"
SOURCE_URL_DESCRIPTOR = "//h3/a/@href"
GENRES_DESCRIPTOR = '//div[@class = "tile-info"]//a[@class = "element-link"]/text()'
IMG_URL_DESCRIPTOR = '//img[contains(@class, "lazy")]/@data-original'

ALT_TITLE_URL = "//h4[@title]//text()"
