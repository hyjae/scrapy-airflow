# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockPrice(scrapy.Item):
    symb = scrapy.Field()
    xymd = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    clos = scrapy.Field()
    diff = scrapy.Field()
    rate = scrapy.Field()
    gvol = scrapy.Field()
