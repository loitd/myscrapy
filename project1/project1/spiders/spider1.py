#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project Name: spiders - Created Date: Thursday September 10th 2020
# Author: loitd - Email: loitranduc@gmail.com
# Description: This is a short project/file description
# Copyright (c) 2020 loitd. WWW: https://github.com/loitd
# -----
# Last Modified: Thursday September 10th 2020 12:09:36 am By: loitd
# -----
# HISTORY:
# Date      	By    	Comments
# ----------	------	----------------------------------------------------------
# 2020-09-10	loitd	Initialized
###

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_selenium import SeleniumRequest as SR
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..items import Project1Item, ProductItem

class Spider1Spider(scrapy.Spider):
    '''
    https://docs.scrapy.org/en/latest/topics/spiders.html#crawlspider-example
    scrapy crawl spider1 -o tv.json
    scrapy crawl spider1 -o tv.xlsx
    scrapy crawl spider1 -o tv.csv
    scrapy crawl spider1 -o tv.xml
    '''
    name = 'spider1'
    allowed_domains = ['mediamart.vn']
    # start_urls = ['https://mediamart.vn/tivi/?trang=1']

    def start_requests(self):
        # Get first page
        yield SR(
            url='https://mediamart.vn/tivi/?trang=1', 
            callback=self.parse_tivi,
            wait_time=10,
            wait_until=EC.element_to_be_clickable((By.XPATH, '//ul[@id="pagination"]/li[@class="last"]/a')),
            screenshot=False,
            script='',
        )

    def clean(self, txt):
        txt = txt.replace('\r','')
        txt = txt.replace('\n','')
        txt = txt.strip()
        return txt

    def parse_tivi(self, response):
        # self.logger.warning('[parse_tivi] ===> Started with URL: %s', response.url)
        self.logger.warning('[parse_tivi] ===> Started with URL')
        for product in response.css('li.pl18-item-li'):
            _name = product.css('p.pl18-item-name a::text').get().strip()
            _link = product.css('p.pl18-item-name a::attr(href)').get().strip()
            _brand = product.css('p.pl18-item-brand::text').get()
            _brand = self.clean(_brand)
            _bprice = product.css('div.pl18-item-pbuy::text').get()
            _bprice = self.clean(_bprice)
            _mprice = product.css('div.pl18-item-pmarket::text').get()
            _mprice = self.clean(_mprice)
            # yield {'brand': _brand, 'name': _name, 'bprice': _bprice, 'mprice': _mprice, 'link': _link}
            yield ProductItem(name=_name, brand=_brand, bprice=_bprice, mprice=_mprice, link=_link)
        
        # https://devhints.io/xpath
        # nextpage = response.xpath('//ul[@id="pagination"]/li/text()').get()
        nextpage = response.xpath('//ul[@id="pagination"]/li[@class="last"]/a/@href').get()
        # self.logger.warning('[parse_tivi] ===> NextPage URL: %s', nextpage)
        self.logger.warning('[parse_tivi] ===> NextPage URL')
        if nextpage:
            yield SR(
                url=nextpage, 
                callback=self.parse_tivi,
                wait_time=10,
                wait_until=EC.presence_of_element_located((By.XPATH, '//ul[@id="pagination"]/li[@class="active"]'))
            )
