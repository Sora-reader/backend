from .pipelines import MangaChanPipeline

BOT_NAME = "manga_chan"

SPIDER_MODULES = ["apps.parse.manga_chan.list_parser"]
NEWSPIDER_MODULE = "apps.parse.manga_chan.list_parser"

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
    MangaChanPipeline: 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
