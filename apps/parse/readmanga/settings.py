from apps.parse.readmanga.pipelines import ReadmangaPipeline

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0


BOT_NAME = "readmanga"
SPIDER_MODULES = ["apps.parse.readmanga.list"]
NEWSPIDER_MODULE = "apps.parse.readmanga"

DOWNLOADER_MIDDLEWARES = {
    "apps.parse.scrapy.middleware.ErrbackMiddleware": 340,
    "apps.parse.scrapy.middleware.ProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 400,
}
ITEM_PIPELINES = {
    ReadmangaPipeline: 300,
}

LOG_FILE = "parse-readmanga.log"
