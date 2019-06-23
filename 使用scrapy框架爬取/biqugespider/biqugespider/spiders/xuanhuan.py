# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from biqugespider.items import BiqugespiderItem


class XuanhuanSpider(CrawlSpider):
    name = 'xuanhuan'
    allowed_domains = ['www.sbiquge.com']
    start_urls = ['https://www.sbiquge.com/xuanhuanxiaoshuo/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='l bd']/ul/li/span[@class='s2']/a"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='listmain']/dl/dd/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print(response.text)
        item = BiqugespiderItem()
        book_name = response.xpath("//div[@class='p']/a[2]/text()").extract_first()
        # print(book_name)
        chapter_name = response.xpath("//div[@class='content']/h1/text()").extract_first()
        # print(chapter_name)
        # content = response.xpath("string(//div[@id='content'])").extract()
        content = response.xpath("string(//div[@id='content'])").extract_first()
        # print(content)
        # print(type(content))
        # print(len(content))
        # print(content[0])

        item['book_name'] = book_name
        item['chapter_name'] = chapter_name
        item['content'] = content
        yield item




        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
