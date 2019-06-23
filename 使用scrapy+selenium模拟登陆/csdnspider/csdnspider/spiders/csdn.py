# -*- coding: utf-8 -*-
import scrapy


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['www.csdn.net']
    start_urls = ['https://passport.csdn.net/login', 'https://blog.csdn.net/Gi1gamesh/']
    # 创建一个cookies类变量
    cookies = None
    def parse(self, response):
        if response.url.find('login') == -1:  # start_urls[1] 登陆后的访问url页面才保存
            print(response.text)
            with open('./csdn.html', 'w', encoding='utf-8') as fp:
                fp.write(response.text)
        # return None

