import scrapy
from urlparse import urljoin
import re
from badger2.items import PostItem
import logging
from bs4 import BeautifulSoup
import datetime



class BadgerSpider(scrapy.Spider):
    name = "badger"
    start_urls =['https://www.badgerandblade.com/forum/',
    ]

    def parse(self, response):
        for top_link in response.xpath('//*[@class="menuRow"]|//*[@class="nodeText"]//a').css('::attr(href)').extract():
            names=[]
            names.append(top_link)
            beginingstats=zip(names,response.css('dl.xbNodeDiscussion dd::text').extract(),response.css('dl.xbNodeMessages dd::text').extract())
            self.logger.info(["First count for :{} Discussion:{} Messages:{}".format(x[0],x[1],x[2])for x in beginingstats])
            yield scrapy.Request(response.urljoin(top_link),callback=self.parse_page2)
         
    def parse_page2(self,response):
        for thread_link in response.css('.title a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(thread_link),callback=self.parse_posts)
        
        next_thread_page = response.css('a+ .text ::attr(href)').extract_first()
        if next_thread_page is not None:
            next_thread_page = response.urljoin(next_thread_page)
            yield scrapy.Request(next_thread_page, callback=self.parse_page2)
        else:
            last_page= response.xpath('//link[@rel="canonical"]').css('::attr(href)').extract_first()
            thread_count=response.css('.contentSummary::text').extract_first()
            if thread_count is not None:
                count=re.sub('^.*of ','',thread_count)
                self.logger.info('Finished forum page requests at:{0} Second thread count:{1}'.format(last_page,count))

    def parse_posts(self,response):
        for posts in response.css('#content .pageContent'):
            item=PostItem()
            ##Getting rid of asides,links and html
            cleanposts=[]
            post = posts.css('.messageText').extract()
            for x in post:
                soup=BeautifulSoup(x,"lxml")
                for aside in soup('aside'):
                   aside.decompose()
                for links in soup(href=True):
                    links.decompose()
                cleanposts.append(" ".join((soup.get_text()).split()).encode('ascii','ignore'))
            ### clean and encode numbers 
            nums=[x.replace('#','').encode('ascii','ignore') for x in posts.css('#messageList .OverlayTrigger::text').extract()]
            ##encode authors
            encodedauths=[x.encode('ascii','ignore').replace(' ','_') for x in response.xpath('//h3[@class="userText"]').css('a::text').extract()]
            ###above was using posts.css('#messageList .username::text') but miss indexing occured due to posts including @username. The above has fixed that
            ##encoded dates
            uglydates=[re.sub(r'.at.*$','',x) for x in response.xpath('//span[@class="leftSide"]').css('.DateTime::text').extract()]
            dates=[datetime.datetime.strptime(x,'%b %d, %Y').strftime('%m/%d/%Y') for x in uglydates]
            #path https://www.badgerandblade.com/forum/threads/[thread#] leads to each thread
            mypath=response.xpath('//p[@id="pageDescription"]').css('a::attr(href)').extract()
            ##This puts forum title \t forum# \t thread title \t thread
            item['path']='{}\t{}'.format(mypath[0].replace('fourms/','').replace('.','\t').replace('/',''),mypath[-1].replace('threads/','').replace('.','\t').replace('/','')).encode('ascii','ignore')
            #https://www.badgerandblade.com/forum/posts/[post#] gives a url for each post
            post_number=[x.replace('post-','').encode('ascii','ignore') for x in response.xpath('//ol[@class="messageList xbMessageDefault"]').css('li::attr(id)').extract()]
            for b,c,d,e,f in zip(dates,nums,encodedauths,cleanposts,post_number):
                item['date']=b
                item['number']=c
                item['author']=d
                item['post']=e
                item['post_numbers']=f
                yield item


        next_page = response.css('a+ .text ::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_posts)


