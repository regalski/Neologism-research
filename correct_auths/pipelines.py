# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import items
import re
import csv
class CsvPipeline(object):

    def process_item(self, item, spider):
        with open('/home/dyslexicon/correct_auths/postid.correct_auth.txt','a+b') as csvfile:
            csvfile.write('{}\t{}\t{}\n'.format(item['post_id'],item['author'],item['post_number']))
