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
from scrapy.selector import XmlXPathSelector 

from urllib import quote, unquote
from yaml import load, dump
from datetime import datetime
from scrapy_service.parsers.HTMLParser import HtmlParser
from scrapy_service.databases.mongo import Mongodb
from scrapy_service.items import ScrapyServiceItem
from pybloom import BloomFilter

class product_spider_object_type_xml(CrawlSpider):
    # Default Data should be config in spiders
    name = "Product_Spider_Lazada"
    allowed_domains = []
    start_urls = []
    # rules = (
    # )

    # My Extra DATA
    data = []
    name_data = ''
    source = ''


     # Init Spider
    def __init__(self, *arg, **karg):
        self.init_yaml('scrapy_service/templates/product.yaml','lazada_sitemap')
        CrawlSpider.__init__(self, *arg)

    # Load information form YAML file
    def init_yaml(self, path_to_file, name_data):
        document = open(path_to_file, 'r')
        self.data = load(document)
        self.name_data = name_data
        self.source = self.data[self.name_data]['database']['name']
        document.close()
        
        self.allowed_domains = self.data[self.name_data]['allowed_domains']
        self.start_urls = self.data[self.name_data]['start_urls']
       
        # Get Links by Rule. This can be NULL
        temp_rule = []
        for rule in self.data[self.name_data]['pattern']:
            temp_rule.append(Rule(LinkExtractor(allow=(rule, )), callback='parse'))
        self.rules = set(temp_rule)
        self.crawled_links = BloomFilter(2000000,0.00001)

    def parse(self, response):
        xpath_selector = HtmlXPathSelector(response)
        
        # Check to parse more links
        if response.headers.get('Content-Type',False) and 'xml' in response.headers['Content-Type']:
            extra_links = HtmlParser.extract_new_link_with_xpath(self.data[self.name_data], xpath_selector)
            for link in extra_links:
                current_link = link if 'http' in link else self.start_urls[0]+ link
                if current_link not in self.crawled_links:
                    self.crawled_links.add(current_link)
                    yield Request(current_link, callback=self.parse)
        else:
            ### Get ALL Items which existing in the current link 
            items = HtmlParser.extract_product_with_xpath(self.data[self.name_data], xpath_selector, self.source)
            for item in items:
                yield item
        


class product_spider_lazada(product_spider_object_type_xml):
    def __init__(self, *arg, **karg):
        product_spider_object_type_xml.__init__(self, *arg, name='lazada_sitemap')