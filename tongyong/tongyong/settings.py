# -*- coding: utf-8 -*-



BOT_NAME = 'tongyong'

SPIDER_MODULES = ['tongyong.spiders']
NEWSPIDER_MODULE = 'tongyong.spiders'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 16
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

SPIDER_MIDDLEWARES = {

    'tongyong.middlewares.tongyongDownloaderMiddleware': 542,

}

DOWNLOADER_MIDDLEWARES = {
   'tongyong.middlewares.tongyongProxyMiddleWare': 543,
    'tongyong.middlewares.tongyongSpiderMiddleware': 542,
    'tongyong.middlewares.RotateUserAgentMiddleware': 541,

}

ITEM_PIPELINES = {
   #'tongyong.pipelines.MysqlTwistedPipeline': 300,
    'tongyong.pipelines.EsserachPipeline': 310
}
# 在redis中保持scrapy-redis用到的队列，不会清理redis中的队列，从而可以实现暂停和恢复的功能。
#SCHEDULER_PERSIST = True

#COMMANDS_MODULE = 'tongyong.commands'#scrapy crawlall运行全部
