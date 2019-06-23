# -*- coding: utf-8 -*-
import json
import re

import scrapy
from bs4 import BeautifulSoup
from jsonpath import jsonpath

from eastmoney.items import EastmoneyItem


class SzaguSpider(scrapy.Spider):
    name = 'szAgu'
    allowed_domains = ['quote.eastmoney.com', 'f10.eastmoney.com', 'nufm.dfcfw.com']
    # start_urls = ['http://quote.eastmoney.com/center/gridlist.html#sz_a_board']
    start_urls = ['http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112405289668058799641_155'
                  '9294230463&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2Cr'
                  'ecordsFiltered%3A(tot)%7D)&cmd=C._SZAME&st=(ChangePercent)&sr=-1&p=1&ps=20']

    def parse(self, response):       # parse方法 会默认接收请求start_urls中地址返回的response
        # 1. 使用selenium
        # # print(response.text)   # 打印获取的源码依然没有想要的数据,但selenium的page_source方法获取的html对象可以直接进行解析
        # # xpath 无法使用, 网页的元素路径一直在刷新,使用beautifulsoup进行解析
        # # company = response.xpath("/table[@id='main-table']/tbody/tr[@class='odd'][3]/td[@class='listview-col-Name']/text()").extract()
        # soup = BeautifulSoup(response.text, 'lxml')
        # companys = soup.select('.listview-col-Code a')
        # for company in companys:
        #     # company_url = company.get('href')
        #     code = company.string
        #     # url = 'http://quote.eastmoney.com' + company_url
        #     url = f'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax?code=SZ{code}' # 直接请求真地址(ajax请求的地址)
        #     yield scrapy.Request(url=url, callback=self.parse_detail)


        # 2.使用直接请求 ajax动态请求的地址的方法
        result = re.findall('jQuery.*\((.*)\)', response.text, re.S)[0]
        res = result.replace('data', '"data"').replace('recordsFiltered', '"recordsFiltered"')
        dic = json.loads(res)
        for info in dic.get('data'):
            code = info.split(',')[1]
            url = f'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax?code=SZ{code}'  # 直接请求真地址(ajax请求的地址)
            yield scrapy.Request(url=url, callback=self.parse_detail)

        # 爬取下一页
        for i in range(2, 11):
            url = f'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112405289668058799641_' \
                f'1559294230463&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%' \
                f'2CrecordsFiltered%3A(tot)%7D)&cmd=C._SZAME&st=(ChangePercent)&sr=-1&p={i}&ps=20'
            yield scrapy.Request(url=url, callback=self.parse)


    # 多余的
    # def parse_detail_url(self, response):
    #     # 公司概况url,假地址,数据部分为ajax加载,源码没有想要的数据,但可以通过配合selenium获取源码
    #     # overview_url = response.xpath("//div[@class='cells'][1]/a[2]/@href").extract_first()  # 假地址
    #
    #     code = response.xpath("//b[@id='code']/text()").extract_first() # A股代码
    #     # ajax请求的地址
    #     overview_url = f'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax?code=SZ{code}' # 真地址
    #     return scrapy.Request(url=overview_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = EastmoneyItem()
        # print(response)  # ajax加载,响应数据为json类型, 这是一个HtmlResponse,没有方法json()
        data = json.loads(response.text)  # 将json字符串转为字典
        company_name = jsonpath(data, '$.jbzl.gsmc')[0]
        Agu_code = jsonpath(data, '$.jbzl.agdm')[0]
        Agu_brief = jsonpath(data, '$.jbzl.agjc')[0]
        company_brief = jsonpath(data, '$.jbzl.gsjj')[0].strip()
        business_scope = jsonpath(data, '$.jbzl.jyfw')[0]

        item['company_name'] = company_name
        item['Agu_code'] = Agu_code
        item['Agu_brief'] = Agu_brief
        item['company_brief'] = company_brief
        item['business_scope'] = business_scope

        yield item

