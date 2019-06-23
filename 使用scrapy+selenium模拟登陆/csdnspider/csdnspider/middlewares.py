# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

import requests
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from fake_useragent import UserAgent

ua = UserAgent()

class CsdnspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CsdnspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 自定义中间件
class CsdnDownloaderMiddleware(object):
    def process_request(self, request, spider):
        # 思路: 先使用selenium去模拟登录, 然后取出登录之后的cookies
        # 把cookies设置到session中,然后用session去访问登录之后需要爬取的页面即可.
        # 先判断是否是登录url.
        print(request.url) # 将得到当前请求的url
        if request.url.find('login') != -1:  # str.find('s') 找不到返回-1
            # 表示找到, 执行模拟登陆操作
            driver = webdriver.Chrome()
            driver.get(request.url)
            driver.implicitly_wait(10)  # 最多等10秒进行加载, 期间一旦加载出来后立马取消等待
            driver.find_element_by_link_text('账号登录').click()
            phone = driver.find_element_by_id('all')
            phone.send_keys('13875045745')
            password = driver.find_element_by_id('password-number')
            password.send_keys('Yds8012427149.')
            driver.find_element_by_tag_name('button').click()
            # print(driver.get_cookies())  # 获取登陆后的所有cookies ,形式如下
            # [{'domain': '.csdn.net', 'expiry': 1735689545.779095, 'httpOnly': False, 'name': 'uuid_tt_dd', 'path': '/', 'secure': False, 'value': '10_19030935030-1559037557910-753767'}, {'domain': '.csdn.net', 'expiry': 1559051903.107487, 'httpOnly': False, 'name': 'dc_tos', 'path': '/', 'secure': False, 'value': 'ps7l1b'}, {'domain': '.csdn.net', 'expiry': 1735689545.779147, 'httpOnly': False, 'name': 'dc_session_id', 'path': '/', 'secure': False, 'value': '10_1559037557910.706256'}, {'domain': '.csdn.net', 'httpOnly': True, 'name': 'SESSION', 'path': '/', 'secure': False, 'value': 'f9013325-e1e4-4b2b-a8fb-8bf11fe671be'}]

            # 使用spider的类变量存储获得的cookies, 给CsdnSpider类动态设置一个cookies类属性, 以便访问登陆后的url时使用
            spider.cookies = driver.get_cookies()
            body = driver.page_source.encode()  # HtmlResponse对象的参数 body 必须为byte类型
            time.sleep(10)
            driver.quit()
            # 返回构造response对象
            return HtmlResponse(url=request.url, body=body, encoding='utf-8')
        else:  # 使用带cookie的session对象去访问页面
            # 这里使用requests包自己构造请求, 需要自己配置请求头信息
            # headers = {
            #             #     'User-Agent': ua.random,
            #             #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #             #     'Accept-Language': 'en',
            #             # }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
                'Referer': 'https://www.csdn.net/',
                'Accept - Encoding': '',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Host': 'blog.csdn.net'
            }
            session = requests.Session()
            # session.verify = False # 遇到ssl错误,不作证书判断
            for cookie in spider.cookies:
                session.cookies.set(cookie['name'], cookie['value']) # 存放cookie到session

            resp = session.get(request.url, headers=headers)
            return HtmlResponse(url=request.url, body=resp.content, encoding='utf-8')
















