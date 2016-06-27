# -*- coding: utf-8 -*-
from scrapy_service.items import ScrapyServiceItem
from scrapy_service.items import NewScrapyServiceItem

from scrapy.selector import HtmlXPathSelector

class HtmlParser:    
    @staticmethod
    def extract_product_with_xpath(yaml_data_dict, xpath_selector, source):
        """
        yaml_data_dict : a dictionary contains patterns to parse  
        xpath_selector : body web page(html)
        source : where did they come from? 
        """
        items = []
        try:
            products = yaml_data_dict['products']
            for i in products: 
                divs = xpath_selector.select(products[i]['tag_contain'])
                for div in divs:
                    name = ''.join(div.select(products[i]['details']['name']).extract())
                    normal_price = ''.join(div.select(products[i]['details']['normal_price']).extract())
                    discount_price = ''.join(div.select(products[i]['details']['discount_price']).extract())
                    categories = div.select(products[i]['details']['categories']).extract()
                    item = ScrapyServiceItem()
                    item['name'] = name.strip()
                    item['description'] = ''
                    item['normal_price'] = normal_price.strip()
                    item['discount_price'] = discount_price.strip()
                    item['categories'] = [category.strip() for category in categories]
                    item['source'] = source
                    items.append(item)
        except Exception as e:
            print e
            pass

        return items

    @staticmethod
    def extract_new_link_with_xpath(yaml_data_dict, xpath_selector):
        """
        yaml_data_dict : a dictionary contains patterns to parse  
        xpath_selector : body web page(html)
        """
        links = []
        try:
            extra_links = xpath_selector.select(yaml_data_dict['extra_link'])
            for link in extra_links:
                links.append(link.extract())
        except Exception as e:
            print e
            pass
        return links

    @staticmethod
    def extract_link_to_product_with_xpath(yaml_data_dict, xpath_selector):
        """
        yaml_data_dict : a dictionary contains patterns to parse  
        xpath_selector : body web page(html)
        """
        links = []
        try:
            extra_links = xpath_selector.select(yaml_data_dict['link_to_product'])
            for link in extra_links:
                links.append(link.extract())
        except Exception as e:
            print e
            pass
        return links

    @staticmethod
    def extract_details_product_with_xpath(yaml_data_dict, xpath_selector, source):
        """
        yaml_data_dict : a dictionary contains patterns to parse  
        xpath_selector : body web page(html)
        source : where did they come from? 
        """
        items = []
        try:
            products = yaml_data_dict['products']
            for i in products: 
                divs = xpath_selector.select(products[i]['tag_contain'])
                for div in divs:
                    name = ''.join(div.select(products[i]['details']['name']).extract())
                    normal_price = ''.join(div.select(products[i]['details']['normal_price']).extract())
                    discount_price = ''.join(div.select(products[i]['details']['discount_price']).extract())
                    provider = ''.join(div.select(products[i]['details']['provider']).extract())
                    categories = div.select(products[i]['details']['categories']).extract()
                    item = NewScrapyServiceItem()
                    item['name'] = name.strip()
                    item['normal_price'] = normal_price.strip()
                    item['discount_price'] = discount_price.strip()
                    item['provider'] = provider.strip()
                    item['categories'] = [category.strip() for category in categories]
                    item['source'] = source
                    items.append(item)
        except Exception as e:
            print e
            pass

        return items


