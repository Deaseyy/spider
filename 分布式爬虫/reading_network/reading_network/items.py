# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReadingNetworkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pic_url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    auth = scrapy.Field()
    book_brief = scrapy.Field()
    auth_brief = scrapy.Field()
    buy_site = scrapy.Field()

