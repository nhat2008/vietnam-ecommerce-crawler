# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from databases.es import ES
from datetime import datetime

class ScrapyServicePipeline(object):

    def __init__(self):
        today_string = (datetime.today()).strftime("%m_%d_%Y")  
        self.database_product = ES(index='scrapy_'+today_string, doc_type='product')

    def process_item(self, item, spider):
        if self.check_quality_product(item):
            self.database_product.save(dict(item))
        return item

    def check_quality_product(self, item):
        if item.get('name',False) and item['name'] not in ['', ' '] and  (item.get('normal_price',False) or item.get('discount_price',False)):
            return True
        return False
