# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymysql
from scrapy.utils.project import get_project_settings


class ReadingNetworkPipeline(object):
    # 写入json文件
    # 开启爬虫时执行
    def open_spider(self, spider):
        self.fp = open('./guoxue.json', 'w+', encoding='utf-8')
        self.fp.write('[\n')

    # 返回item后执行
    def process_item(self, item, spider):
        self.fp.write(json.dumps(dict(item), ensure_ascii=False) + ', \n')
        return item

    # 爬虫关闭时调用
    def close_spider(self,spider):
        self.fp.write(']')
        self.fp.close()


# 存入数据库
class ReadingNetworkMysqlPipeline(object):  # 需添加到settings管道配置
    def open_spider(self,spider):
        # 创建连接
        settings = get_project_settings()  # 封装好的获取配置文件settings的方法
        host = settings.get('DB_HOST')
        port = settings.get('DB_PORT')
        user = settings.get('DB_USER')
        password = settings.get('DB_PASSWORD')
        database = settings.get('DB_DATABASE')
        charset = settings.get('DB_CHARSET')
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password,
                               database=database, charset=charset)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))  # '%s, %s, %s'
        sql = f'insert into guoxue({keys}) values({values})'
        print(222)
        try:
            self.cursor.execute(sql, tuple(data.values()))  # 传一个元组 替换 其中%s
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


