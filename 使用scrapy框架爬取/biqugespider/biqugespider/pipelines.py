# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os


class BiqugespiderPipeline(object):

    # # 写入json文件
    # # 开启爬虫时执行
    # def open_spider(self, spider):
    #     self.fp = open('./xh.json', 'w+', encoding='utf-8')
    #     self.fp.write('[\n')
    #
    # # 返回item后执行
    # def process_item(self, item, spider):
    #     self.fp.write(json.dumps(dict(item), ensure_ascii=False) + ', \n')
    #     return item
    #
    # # 爬虫关闭时调用
    # def close_spider(self, spider):
    #     self.fp.write(']')
    #     self.fp.close()



    # 写入txt文件
    def process_item(self, item, spider):
        book_name = item['book_name']
        chapter_name = item['chapter_name']
        content = item['content']
        # print(os.getcwd())
        with open('biqugespider/xiaoshuo/' + book_name + '.txt', 'a', encoding='utf-8') as f:
            f.write(chapter_name + '\n' + content +'\n\n\n')
        return item


