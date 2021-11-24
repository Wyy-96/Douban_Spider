from selenium import webdriver

import time  # from selenium.webdriver.common.keys import Keys

# chromedriver.exe的地址，因为添加到了环境变量，所以不用填绝对地址


def getCookies():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://accounts.douban.com/passport/login?source=movie")

    time.sleep(5)
    driver.find_element_by_xpath(
        '//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()  # //*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]

    username = driver.find_element_by_name('username')
    username.clear()
    time.sleep(2)
    username.send_keys('15958015173')  # xxx为用户名

    password = driver.find_element_by_name('password')
    time.sleep(2)
    password.send_keys('19961108xx')  # xxx为密码

    driver.find_element_by_xpath(
        '//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()

    time.sleep(20)
    cookie = {}
    for item in driver.get_cookies():
        cookie[item['name']] = item['value']
    
    return cookie
