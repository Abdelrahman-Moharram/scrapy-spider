import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property
from scrapy.crawler import CrawlerProcess
import json

import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            print(start_url)
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.getPaginationPage)
    
    def getPaginationPage(self, response):
        for page in response.xpath('.//div[contains(@class,"pagination")]/ul/li/a[contains(@href,text())]/@href').extract() :
            yield Request(url=page,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):

        


        for area in  response.xpath('.//div[contains(@class,"right-cont")]'):
            property = ItemLoader(item=Property(),  selector=area)
            property.add_xpath('title', './/div/h4/a/text()')
            property.add_xpath('price', './/div[contains(@class,"bottom-ic")]/h5/text()')
            property.add_xpath('url', './/div/h4/a/@href')
            return property.load_item()

        

process = CrawlerProcess()
process.crawl(LondonrelocationSpider)
process.start()