# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PostItem(scrapy.Item):
    # define the fields for your item here like:
    thread = scrapy.Field()
    number=scrapy.Field()
    author=scrapy.Field()
    date = scrapy.Field()
    post=scrapy.Field()
    path=scrapy.Field()
    post_numbers=scrapy.Field()
    pass
