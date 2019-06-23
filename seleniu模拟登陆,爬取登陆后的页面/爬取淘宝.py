import time

import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains, ChromeOptions
from selenium.webdriver.chrome.options import Options

# 添加chrome选项参数
# cmd执行: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
    # 参数: -remote-debugging-port 可以指定任何打开的端口。-user-data-dir标记，指定创建新Chrome配置文件的目录。
    # 它是为了确保在单独的配置文件中启动chrome，不会污染你的默认配置文件。不要忘了在环境变量中PATH里将chrome的路径添加进去。
# 先打开淘宝,正常手动登陆, 然后再使用selenium接管当前状态的浏览器,进行后面的工作.
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(chrome_options=chrome_options)
# action = ActionChains(driver)

# url = 'https://login.taobao.com/'
url = 'https://www.taobao.com/'
driver.get(url)

# 跳过自动登陆, 手动登陆
# pwd_login = driver.find_element_by_css_selector('.forget-pwd.J_Quick2Static')
# pwd_login.click()
# time.sleep(5)
# name = driver.find_element_by_id('TPL_username_1')
# name.send_keys('13875045745')
# time.sleep(1)
# pwd = driver.find_element_by_id('TPL_password_1')
# pwd.send_keys('yds8012427149')
# time.sleep(1)
# slider = driver.find_element_by_id('nc_1_n1z')
# action.drag_and_drop_by_offset(slider, 258, 0).perform()  # 拖动滑块258px,根据css样式width变动获取
# login_btn = driver.find_element_by_id('J_SubmitStatic')
# login_btn.click()
# time.sleep(0.5)

driver.find_element_by_id('q').send_keys('手机')
driver.find_element_by_css_selector('.btn-search.tb-bg').click()
driver.implicitly_wait(5)  # 隐式等待  等待数据加载

# 滚动滚轮    某些数据随滚轮动态加载, 需先滚动加载完页面,再用page_sourse获取源码
distance = driver.execute_script('var distance=document.body.scrollHeight;return distance;') # 获取页面高度
offset = 0
while offset < distance:
    driver.execute_script(f'window.scrollTo({offset}, {offset+10} )')
    offset += 10
time.sleep(2)

html = driver.page_source # 获取网页源码 和requests请求响应的html不同的是可以直接对节点操作
soup = BeautifulSoup(html, 'lxml')
results = soup.select('.item.J_MouserOnverReq')
content = []
for result in results:
    result = str(result)
    soup2 = BeautifulSoup(result, 'lxml')
    # pic_url = soup2.select('img.J_ItemPic.img')[0]['src']
    pic_url = soup2.select('img[id^="J_Itemlist_Pic"]')[0].get('src')
    print(pic_url)
    raw_title = soup2.select('.row.row-2.title .J_ClickStat')[0].get_text().strip()
    view_price = soup2.select('.price.g_price.g_price-highlight strong')[0].string
    view_sales = soup2.select('div.deal-cnt')[0].string
    nick = soup2.select('a.shopname.J_MouseEneterLeave.J_ShopInfo > span')[1].string
    item_loc = soup2.select('div.location')[0].string
    dic = {'商品图': pic_url,
           '商品名称': raw_title,
           '价格': view_price,
           '付款人数': view_sales,
           '店铺名': nick,
           '所在地': item_loc
           }
    content.append(dic)
print(content)

# 仅仅爬取了首页














