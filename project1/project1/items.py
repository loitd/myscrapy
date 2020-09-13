#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project Name: project1 - Created Date: Thursday September 10th 2020
# Author: loitd - Email: loitranduc@gmail.com
# Description: This is a short project/file description
# Copyright (c) 2020 loitd. WWW: https://github.com/loitd
# -----
# Last Modified: Thursday September 10th 2020 12:05:10 am By: loitd
# -----
# HISTORY:
# Date      	By    	Comments
# ----------	------	----------------------------------------------------------
# 2020-09-10	loitd	Initialized
###

import scrapy
from scrapy import Field, Item


class Project1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductItem(Item):
    name = Field()
    brand = Field()
    bprice = Field()
    mprice = Field()
    link = Field()