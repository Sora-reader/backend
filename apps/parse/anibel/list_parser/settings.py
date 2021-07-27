from apps.parse.anibel.list_parser.pipelines import AnibelPipeline

BOT_NAME = "anibel"

SPIDER_MODULES = ["apps.parse.anibel.list_parser"]
NEWSPIDER_MODULE = "apps.parse.anibel.list_parser"

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
    AnibelPipeline: 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
