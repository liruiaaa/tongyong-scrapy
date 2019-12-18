# -*- coding: utf-8 -*-
import scrapy
import time
import re
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tongyong.items import TongyongItem

class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/p/.+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        item = TongyongItem()
        timeArrays = time.localtime(int(time.time()))
        gtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArrays)
        item['gtime'] = gtime
        item['url']=response.url
        item['site_name']='简书'
        item['title'] = response.xpath('//h1[contains(@class,"_1RuRku")]/text()').get()
        try:
            nums=re.findall('"views_count":(\d+)',response.text)
            item['read_num'] = nums[-1]
        except:
            item['read_num']=0
        try:
            ctimes = re.findall('"first_shared_at":(\d+)', response.text)
            timeStamp = int(ctimes[-1])
            timeArray = time.localtime(timeStamp)
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            item['ctime'] = ctime
        except:
            item['ctime']=gtime

        item['author'] = response.xpath('//span[@class="_22gUMi"]/text()').get()
        contents = response.xpath('//article[contains(@class,"_2rhmJa")]/p/text()').getall()
        content_text = ''.join(contents)
        content_text = re.sub(" |\t|\n|\r|\r\n", " ", content_text).strip()
        content_text = re.sub("\s+", " ", content_text).strip()
        item['content'] = content_text

        return item
