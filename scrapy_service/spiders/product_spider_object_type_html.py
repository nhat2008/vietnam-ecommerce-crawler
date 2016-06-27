# -*- coding: utf-8 -*-
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from urllib import quote, unquote
from yaml import load, dump
from datetime import datetime
from scrapy_service.parsers.HTMLParser import HtmlParser
from scrapy_service.databases.mongo import Mongodb
from scrapy_service.databases.es import ES

from scrapy_service.items import ScrapyServiceItem

from pybloom import BloomFilter

# This class can be used for the website having template like comparevn, websosanh 
# Check template in product.yml
class product_spider_object_type_html(CrawlSpider):
    # Default Data should be config in spiders
    name = None
    allowed_domains = []
    start_urls = []

    rules = (
    )
    
    # My Extra DATA
    data = []
    name_data = ''
    source = ''
    crawled_links = None


     # Init Spider
    def __init__(self, *arg, **karg):
        self.name = karg['name']
        self.init_yaml('scrapy_service/templates/product.yaml',self.name)
        CrawlSpider.__init__(self, *arg)

    # Load information form YAML file
    def init_yaml(self, path_to_file, name_data):
        """
        path_to_file : path to template file
        name_data : name template in the template file
        """
        
        document = open(path_to_file, 'r')
        self.data = load(document)
        self.name_data = name_data
        self.source = self.data[self.name_data]['database']['name']
        document.close()
        
        self.allowed_domains = self.data[self.name_data]['allowed_domains']
        self.start_urls = self.data[self.name_data]['start_urls']


        # Get Links by Rule
        temp_rule = []
        for rule in self.data[self.name_data]['pattern']:
            temp_rule.append(Rule(LinkExtractor(allow=(rule, )), callback='my_parse'))
        self.rules = set(temp_rule)
        self.crawled_links = BloomFilter(2000000,0.00001)

    def my_parse(self, response):
        xpath_selector = HtmlXPathSelector(response)
        ### Get ALL Items which existing in the current link 
        items = HtmlParser.extract_details_product_with_xpath(self.data[self.name_data], xpath_selector, self.source)
        for item in items:
            yield  item

        ## Get All Links which existing in the current link
        extra_links = HtmlParser.extract_new_link_with_xpath(self.data[self.name_data], xpath_selector)
        for link in extra_links:
            current_link = link if 'http' in link else self.start_urls[0]+ link
            if current_link not in self.crawled_links:
                self.crawled_links.add(current_link)
                yield Request(current_link, callback=self.my_parse)


        ## Get Links to details product
        links_to_product = HtmlParser.extract_link_to_product_with_xpath(self.data[self.name_data], xpath_selector)
        for link in links_to_product:
            current_link = link if 'http' in link else self.start_urls[0]+ link
            if current_link not in self.crawled_links:
                self.crawled_links.add(current_link)
                yield Request(current_link, callback=self.my_parse)


class product_spider_compare(product_spider_object_type_html):
    def __init__(self, *arg, **karg):
        product_spider_object_type_html.__init__(self, *arg, name='compare')

class product_spider_websosanh(product_spider_object_type_html):
    def __init__(self, *arg, **karg):
        product_spider_object_type_html.__init__(self, *arg, name='websosanh')

class product_spider_cdiscount(product_spider_object_type_html):
    def __init__(self, *arg, **karg):
        product_spider_object_type_html.__init__(self, *arg, name='cdiscount')
        
class product_spider_cungmua(product_spider_object_type_html):
    def __init__(self, *arg, **karg):
        product_spider_object_type_html.__init__(self, *arg, name='cungmua')

class product_spider_hotdeal(product_spider_object_type_html):
    def __init__(self, *arg, **karg):
        product_spider_object_type_html.__init__(self, *arg, name='hotdeal')
