# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScrapyServiceItem(Item):
    name = Field()
    description = Field()
    normal_price = Field()
    discount_price = Field()
    source = Field()
    categories = Field()


class NewScrapyServiceItem(Item):
    name = Field()
    normal_price = Field()
    discount_price = Field()
    source = Field()
    provider = Field()
    categories = Field()
