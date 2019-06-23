from selenium import webdriver

driver = webdriver.Chrome()


url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
driver.get(url)

email = driver.find_element_by_id('email')
email.send_keys('13875045745')

pwd = driver.find_element_by_id('pwd')
pwd.send_keys('Yds8012427149.')

randcode = driver.find_element_by_id('code')
driver.save_screenshot('./bigyzm.png')
yzm = input('请输入验证码:')
randcode.send_keys(yzm)

login = driver.find_element_by_id('denglu')
login.click()





