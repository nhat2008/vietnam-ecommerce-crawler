__author__ = 'nhat'
from scrapy.utils.project import get_project_settings

from scrapy_service.spiders.product_spider_object_type_html import product_spider_websosanh
from scrapy_service.spiders.product_spider_object_type_html import product_spider_compare
from scrapy_service.spiders.product_spider_object_type_html import product_spider_cdiscount
from scrapy_service.spiders.product_spider_object_type_html import product_spider_hotdeal
from scrapy_service.spiders.product_spider_object_type_html import product_spider_cungmua


from scrapy_service.spiders.product_spider_object_type_xml import product_spider_lazada

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import threading
import time

# creat asynchronous function with decorator
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(product_spider_hotdeal)
    reactor.stop()

# Because preventing the scrapy run too long time, we will set time to stop 
def stop_crawler(hour=4):
    time.sleep(hour*60*60)
    reactor.stop()


if __name__ == '__main__':
    try:
        # Get cunrrent settings in settings.py
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        
        # Set time to stop after x hours
        # stop_threading = threading.Thread(target=stop_crawler, args=(4,))
        # stop_threading.start()
        
        crawl()
        reactor.run() # the script will block here until the last crawl call is finished
    except Exception as e:
        print e
        pass