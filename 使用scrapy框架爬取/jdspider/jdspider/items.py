# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    pic_url = scrapy.Field()
    money = scrapy.Field()
    describe = scrapy.Field()
    shop_name = scrapy.Field()
    comment_num = scrapy.Field()


# class comments

