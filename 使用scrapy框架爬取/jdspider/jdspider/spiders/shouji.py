# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from jdspider.items import JdspiderItem
from scrapy_redis.spiders import RedisSpider


# class ShoujiSpider(scrapy.Spider):
#     name = 'shouji'
#     allowed_domains = ['www.jd.com']
#     start_urls = ['https://www.jd.com/']


class ShoujiSpider(RedisSpider):
    name = 'shouji'

    redis_key = 'start_urls'

    def parse(self, response):
        item = JdspiderItem()
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        shop_name = soup.select('.curr-shop')
        # print(shop_name)
        money = soup.select('.p-price strong i')
        # print(money)
        pic_url = soup.select('.p-img a img')
        # print(pic_url)
        describes = soup.select('.p-name.p-name-type-2 a em')
        # print(describes)
        comment_nums = soup.select('strong a')
        # print(comment_nums)
        detail_url = soup.select('.p-img a')

        for i in range(len(shop_name)):
            print(shop_name[i].string)
            item['shop_name'] = shop_name[i].string
            print(pic_url[i].get('src'))
            item['pic_url'] = pic_url[i].get('src')
            print(money[i].string)
            item['money'] = money[i].string
            print(describes[i].get_text())
            item['describe'] = describes[i].get_text()
            print(comment_nums[i].string)
            item['comment_num'] = comment_nums[i].string
            yield item
            # print(detail_url[i].get('href'))
            # url = 'https:' + detail_url[i].get('href')
            # yield scrapy.Request(url=url, callback= self.parse_detail)


        # 爬取下一页
        for i in range(3, 50, 2):
            url = f'https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2' \
                f'&suggest=2.def.0.V09--12s0%2C20s0%2C38s0&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page={i}&s={(i-1)*30+1}'
            yield scrapy.Request(url=url, callback=self.parse)

        # shop_name = response.xpath("//a[@class='curr-shop']/text()").extract()
        # print(shop_name)
        # pic_url = response.xpath("//div[@class='p-img']/a/img/@src").extract()
        # print(pic_url)
        # money = response.xpath("//div[@class='p-price']/strong/i/text()").extract()
        # print(money)
        # describes = response.xpath("//div[@class='p-name p-name-type-2']/a/em")
        # comment_nums = response.xpath("//strong/a/text()").extract()
        # print(comment_nums)
        # detail_url = response.xpath("/div[@class='p-name p-name-type-2']/a/@href").extract()
        # print(detail_url)

        # for i in range(len(shop_name)):
        #     item['shop_name'] = shop_name[i]
        #     item['pic_url'] = pic_url[i]
        #     item['money'] = money[i]
        #     # item['describe'] = describes[i]
        #     item['comment_num'] = comment_nums[i]
        #     yield item
            # yield scrapy.Request(url=url, callback=self.parse_detail)


    # def parse_detail(self,response):
    #     soup = response.text()
    #     soup.select('')