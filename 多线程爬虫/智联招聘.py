import json
import queue
import threading
import time

from lxml import etree
from jsonpath import jsonpath
import requests
from requests.exceptions import RequestException
from fake_useragent import UserAgent

lock = threading.Lock()

page_queue = queue.Queue()  # 页码队列  提前放入页码
parse_queue = queue.Queue()  # 解析队列  一边加, 一边取

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

flag = False
class SpiderThread(threading.Thread):
    def __init__(self, page_queue, parse_queue, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.parse_queue = parse_queue
        self.id = id

    def run(self):
        while not page_queue.empty():
            page = self.page_queue.get(block=False)
            url = f'https://fe-api.zhaopin.com/c/i/sou?start={(page-1)*90}&pageSize=90&cityId=765&salary=0,0&workExperience=' \
           '-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3'
            times = 4
            while times > 0:
                try:
                    response = requests.get(url, headers=headers)
                    # 存入parse_queue队列
                    # print(response.json())
                    self.parse_queue.put(response.json())
                    print(f'{self.id}号线程成功爬取了第{page}页数据')
                    time.sleep(1)
                    # task_done在所有工作都做完之后调用.
                    self.page_queue.task_done()
                    break
                except RequestException:
                    print('爬取失败')
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

    def parse(self, data):
        # print(data)
        # print(type(data))
        results = jsonpath(data,'$.data.results')  # [[ ]]
        work = []
        for result in results[0]:  # len(result): 90
            job_name = jsonpath(result,'$..jobName')  # 职位名
            education = jsonpath(result, '$..eduLevel.name')  # 学历
            company = jsonpath(result, '$..company.name')  # 公司名
            salary = jsonpath(result, "$..salary")  # 薪资
            work_exp = jsonpath(result, '$..workingExp.name')  # 工作经验
            work_city = jsonpath(result, '$..city.display')  # 工作城市

            work.append({'job_name': job_name[0],
                         'education': education[0],
                         'company': company[0],
                         'salary': salary[0],
                         'work_exp': work_exp[0],
                         'work_city': work_city[0],
                         })
            # 存入文件
        with lock:
            self.fp.write(json.dumps(work, ensure_ascii=False) + '\n')


def main():
    for i in range(1, 11):
        page_queue.put(i)

    # 启动爬虫线程
    for i in range(3):
        SpiderThread(page_queue, parse_queue, i).start()

    # 启动解析线程
    fp = open('./zl_python.txt', 'a', encoding='utf-8')
    for i in range(3):
        ParseThread(i, parse_queue, fp).start()


    page_queue.join()
    parse_queue.join() #实际就是为了解决不加队列锁可能检测到某一瞬间为空，就退出线程了，还没有执行完，前面线程可能还在往队列加数据
    global flag
    flag = True
    fp.close()


if __name__ == '__main__':
    main()
