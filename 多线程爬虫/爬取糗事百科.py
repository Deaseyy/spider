import json
import threading
import queue
import requests
import time
from fake_useragent import UserAgent
from lxml import etree
from requests.exceptions import RequestException

lock = threading.Lock()

# 生成2个全局队列
page_queue = queue.Queue()   # 页码队列  提前放入页码
parse_queue = queue.Queue()  # 解析队列  一边加, 一边取

base_url = 'https://www.qiushibaike.com/text/page/%d/'

ua = UserAgent()
headers = {
    "User-Agent" : ua.random
}

flag = False # 线程退出标志

class SpiderThread(threading.Thread):
    def __init__(self, page_queue, parse_queue, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.parse_queue = parse_queue
        self.id = id


    def run(self):
        # 不停的从page_queue中取数据,拼成一个有效url,获取数据,并存入parse_queue

        while not self.page_queue.empty():
            page = self.page_queue.get()
            url = base_url % page
            # 出错后,继续爬取该url,给四次重试机会,
            times = 4
            while times > 0:
                try:
                    response = requests.get(url, headers=headers)
                    # 存入parse_queue队列
                    self.parse_queue.put(response.text)
                    print(f'{self.id}号线程成功爬取了第{page}页数据')
                    time.sleep(1)
                    # task_done一定要在所有的相关工作都做完之后才调用.
                    self.page_queue.task_done()
                    break
                except RequestException:
                    print('爬取错误')
                finally:
                    times -= 1


class ParseThread(threading.Thread):
    def __init__(self, id, parse_queue, fp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.parse_queue = parse_queue
        self.fp = fp


    def run(self):
        # 不停的从parse_queue中去取数据,并解析,写入文件
        global flag
        while True:
            if flag:
                break
            try:
                data = self.parse_queue.get(block=False)
                # 解析
                self.parse(data)
                print(f'{self.id}解析线程解析成功')
                self.parse_queue.task_done()
            except queue.Empty:
                pass


    # 解析
    def parse(self,data):
        html = etree.HTML(data)
        divs = html.xpath("//div[@id='content-left']/div[contains(@id, 'qiushi_tag_')]")
        items = []
        for div in divs:
            item = {}
            images = div.xpath('.//div[contains(@class, "author")]//img/@src')[0]
            name = div.xpath('.//h2')[0].text.strip()
            content = div.xpath('string(.//div[@class="content"])').strip()

            item['image'] = images
            item['name'] = name
            item['content'] = content
            items.append(item)

        # 存入文件
        with lock:
            self.fp.write(json.dumps(items, ensure_ascii=False) + '\n')


def main():
    # 往page_queue存10个页码
    for i in range(10):
        page_queue.put(i + 1)

    # 启动爬虫线程
    for i in range(3):
        SpiderThread(page_queue, parse_queue, i+1).start()

    fp = open('./qiubai.json', 'a', encoding='utf-8')
    # 启动解析线程
    for i in range(3):
        ParseThread(i + 1, parse_queue, fp).start()

    # 队列锁必须配合q.task_done() 使用
    page_queue.join() # 需要parse_queue.task_done()的通知,每次取值都会通知,直到取完,然后往下执行
    parse_queue.join()#实际就是为了解决，如果不加队列锁，可能检测到某一瞬间为空，就退出线程了，工作还没有执行完，前面线程可能还在往队列加数据

    global flag
    flag = True
    # 关闭文件
    fp.close()


if __name__ == '__main__':
    main()