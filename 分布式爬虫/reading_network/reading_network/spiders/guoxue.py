# -*- coding: utf-8 -*-
import scrapy

from scrapy_redis.spiders import RedisSpider   # 分布式时使用: RedisCrawlSpider

from reading_network.items import ReadingNetworkItem


item = ReadingNetworkItem()

class GuoxueSpider(RedisSpider):  # 继承RedisSpider  # 分布式时 继承 RedisCrawlSpider
    name = 'guoxue'

    # start_urls = ['https://www.dushu.com/book/1617.html']
    redis_key = 'start_urls'  # 设置存放开始爬取地址的key

    def parse(self, response):
        # detail_urls = response.xpath('//div[@class="img152 float-left margin-right"]/a/img/@data-original').extract()
        detail_urls = response.xpath('//div[@class="book-info"]/h3/a/@href').extract()
        for url in detail_urls:
            detail_url = 'https://www.dushu.com' + url
            # print(detail_url)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)   # 返回封装的请求对象 返回的响应

        # 爬取下一页
        next_url = 'https://www.dushu.com/book/1617_%d.html'
        for i in range(2, 11):
            yield scrapy.Request(url=next_url % i, callback=self.parse)

    # 解析详情页
    def parse_detail(self, response):
        pic_url = response.xpath('//div[@class="pic"]/img/@src').extract()[0]
        title = response.xpath('//div[@class="book-title"]/h1/text()')[0].extract()
        price = response.xpath('//span[@class="num"]/text()')[0].extract()  # [0].extract() 取不到 报错
        auth = response.xpath('//tr[1]/td[2]/a/text()').extract_first()  # extract_first() 取值为空时返回None,不会报错
        book_brief = response.xpath('//div[@class="text txtsummary"]/text()')[0].extract()
        auth_brief = response.xpath('//div[@class="text txtsummary"]/text()').extract_first()
        buy_site = response.xpath("//div[@class='book-details-right bg-mix']/ul/li/a/text()").extract_first()

        item['pic_url'] = pic_url
        item['title'] = title
        item['price'] = price
        item['auth'] = auth
        item['book_brief'] = book_brief
        item['auth_brief'] = auth_brief
        item['buy_site'] = buy_site
        yield item

