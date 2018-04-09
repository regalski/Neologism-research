import scrapy
from urlparse import urljoin
import re
import logging
from correct_auths.items import CorrectAuthsItem
from bs4 import BeautifulSoup
import datetime

class AuthSpider(scrapy.Spider):
    name= 'auth'
    start_urls = ['',]
    

    def parse(self,response):
        item= CorrectAuthsItem()
        post_id=[x.replace('post-','').encode('ascii','ignore') for x in response.xpath('//ol[@class="messageList xbMessageDefault"]').css('li::attr(id)').extract()]
        author=[x.encode('ascii','ignore').replace(' ','_') for x in response.css('#messageList .username::text').extract()]
        #author=[x.encode('ascii','ignore').replace(' ','_') for x in response.xpath('//h3[@class="userText"]').css('a::text').extract()]
        post_number=[x.replace('#','').encode('ascii','ignore') for x in response.css('#messageList .OverlayTrigger::text').extract()]
        if len(post_id)==len(author)==len(post_number):
            for x,y,z in zip(post_id,author,post_number):
                item['post_id']=x
                item['author']=y
                item['post_number']=z
                yield item
        else:
            self.logger.info('Bad news at ' + str(response.url))
        
        next_page = response.css('a+ .text ::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)