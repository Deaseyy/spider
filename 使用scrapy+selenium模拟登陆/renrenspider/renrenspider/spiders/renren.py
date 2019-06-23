# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['www.renren.com']
    start_urls = ['http://www.renren.com/ajaxLogin/login']

    # 发送post请求
    # 需重写start_request(self), 未重写该函数时,默认会使用get请求,可查看源码
    def start_requests(self):
        data = {
            'email': '13875045745',
            # 'origURL': 'http://www.renren.com/home',
            # 'domain': 'renren.com',
            # 'key_id': '1',
            # 'captcha_type': 'web_login',
            'password': 'Yds8012427149.',
        }
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=data)


    def parse(self, response):
        print(response.text)
