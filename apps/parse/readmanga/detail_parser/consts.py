# descriptors for detail manga parser

RSS_TAG = "//head/link[@type='application/rss+xml'][1]/@href"
AUTHORS_TAG = "//span[@class='elem_author ']/a[@class='person-link']/text()"
YEAR_TAG = "//span[@class='elem_year ']/a[@class='element-link'][1]/text()"
TRANSLATORS_TAG = "//span[@class='elem_translator ']/a[@class='person-link']/text()"
ILLUSTRATOR_TAG = '//span[@class = "elem_illustrator "]/a[@class="person-link"]/text()'
SCREENWRITER_TAG = '//span[@class="elem_screenwriter "]/a[@class="person-link"]/text()'
CATEGORY_TAG = '//span[@class = "elem_category "]/a[@class="element-link"]/text()'
DESCRIPTION_TAG = "//meta[@itemprop='description'][1]/@content"
