from apps.parse.readmanga.readmanga.pipelines import ReadmangaPipeline

BOT_NAME = "readmanga"

SPIDER_MODULES = ["apps.parse.readmanga.readmanga.spiders"]
NEWSPIDER_MODULE = "apps.parse.readmanga.readmanga.spiders"

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
    ReadmangaPipeline: 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
