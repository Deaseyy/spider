import pymysql
from redis import Redis
import json

# 从redis中取出数据,然后储存到mysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='450502',
                       charset='utf8', database='spider1')
cursor = conn.cursor()
redis_conn = Redis()


def insert_mysql():
    while 1:
        # 从redis中取数据
        try:
            _, data = redis_conn.brpop('shouji:items', timeout=60)
        except:
            cursor.close()
            conn.close()
            break

        # 转化为python对象
        data = json.loads(data, encoding='utf-8')
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))  # '%s, %s, %s'
        sql = f'insert into shouji({keys}) values({values})'
        try:
            cursor.execute(sql, tuple(data.values()))  # 传一个元组 替换 其中%s
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()


if __name__ == '__main__':
    insert_mysql()