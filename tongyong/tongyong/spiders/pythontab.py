# -*- coding: utf-8 -*-
import scrapy
import redis
import time
import re
from lxml import etree
#extract()
from urllib.parse import urljoin
from tongyong.items import TongyongItem


#scrapy crawl spider_name -s JOBDIR=jobs/001 暂停  重启
class PythontabSpider(scrapy.Spider):


    name = 'pythontab'
    allowed_domains = ['pythontab.com']
    def __init__(self):
        self.start_urls=[
            'https://www.pythontab.com/html/pythonjichu/',#基础教程
            'https://www.pythontab.com/html/pythonhexinbiancheng/',#高级教程
            'https://www.pythontab.com/html/pythonweb/',#python框架
            'https://www.pythontab.com/html/hanshu/',#python函数
            'https://www.pythontab.com/html/pythongui/',#GUI教程
            'https://www.pythontab.com/html/linuxkaiyuan/',#linux教程
        ]
    def get_start_urls(self):
        for i in self.start_urls:
            yield scrapy.Request(
                url=i,
                dont_filter=True,
                callback=self.parse,
            )
    def parse(self, response):
        base_url=response.url
        loops=response.xpath('''//ul[@id="catlist"]//li//a/@href''').extract()
        for aurl in loops:
            post_url=urljoin(base_url,aurl)
            yield scrapy.Request(
            url=post_url,
            dont_filter=True,
            callback=self.parse_detail,
        )
        next_url=response.xpath('''//a[@class="a1"][last()]//@href''').extract()[0]
        next_url=urljoin(base_url,next_url)

        if  next_url:
            yield scrapy.Request(
                url=next_url,
                dont_filter=True,
                callback=self.parse,
            )

    def parse_detail(self,response):
        item = TongyongItem()
        timeArrays = time.localtime(int(time.time()))
        gtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArrays)
        item['gtime'] = gtime
        item['url'] = response.url
        item['site_name'] = 'PythonTab中文网'
        item['title'] = response.xpath('//div[@id="Article"]/h1/text()').get()
        item['read_num'] = ""
        item['ctime'] = gtime
        item['author'] = "PythonTab中文网"
        contents = response.xpath('//div[@id="Article"]//div[@class="content"]//text()').getall()
        content_text = ''.join(contents)
        content_text = re.sub(" |\t|\n|\r|\r\n", " ", content_text).strip()
        content_text = re.sub("\s+", " ", content_text).strip()
        item['content']=content_text

        return item

