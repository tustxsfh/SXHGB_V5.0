# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
import pytesseract
from pytesseract import image_to_string
from selenium.common.exceptions import WebDriverException


# 使用无头模式打开chrome
chrome_options = Options()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.implicitly_wait(60 * 3)
browser.maximize_window()
src = './'

start_time = time.time()
def login(ume, pwd, name):  # 登录函数
    try:
        # 登录页面
        login_url = "https://www.sxgbxx.gov.cn/login"
        browser.get(login_url)

        username = browser.find_element_by_id('userEmail')
        username.send_keys(ume)  # 此处填入账号
        password = browser.find_element_by_id('userPassword')
        password.send_keys(pwd)  # 此处填入密码
        # 获取截图
        browser.get_screenshot_as_file(src+'tempimg/screenshot.png')

        # 获取指定元素位置
        element = browser.find_element_by_id('img')
        left = int(element.location['x'])
        top = int(element.location['y'])
        right = int(element.location['x'] + element.size['width'])
        bottom = int(element.location['y'] + element.size['height'])

        # 通过Image处理图像
        im = Image.open(src+'tempimg/screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save(src+'tempimg/random.png')

        img = Image.open(src+'tempimg/random.png')
        code = pytesseract.image_to_string(img)

        randomcode = browser.find_element_by_id('randomCode')
        randomcode.send_keys(code)
        browser.find_element_by_class_name('bm-lr-btn').click()

        time.sleep(10)
        print(name+'登录成功')

        

    except WebDriverException:
        print("webdriver 异常")
