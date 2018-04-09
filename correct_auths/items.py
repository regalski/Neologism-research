# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CorrectAuthsItem(scrapy.Item):
    # define the fields for your item here like:
    post_id = scrapy.Field()
    author = scrapy.Field()
    post_number= scrapy.Field()
    thread = scrapy.Field()
    pass
