#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project Name: myscrapy - Created Date: Wednesday September 9th 2020
# Author: loitd - Email: loitranduc@gmail.com
# Description: This is a short project description
# Copyright (c) 2020 loitd. WWW: https://github.com/loitd
# -----
# Last Modified: Wednesday September 9th 2020 3:22:33 pm By: loitd
# -----
# HISTORY:
# Date      	By    	Comments
# ----------	------	----------------------------------------------------------
# 2020-09-09	loitd	Initialized
###

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class MainScrapy(scrapy.Spider):
    # scrapy runspider main.py -o titles.json
    name = "MainScrapy"
    start_urls = ['https://getbootstrap.com/']

    def parse(self, response):
        for title in response.css('header.navbar .navbar-nav-scroll li.nav-item'):
            yield {'title': title.css('a.nav-link::text').get()}

def sampleSelector():
    pass