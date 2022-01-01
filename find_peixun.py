# -*- coding: utf-8 -*-
import time,os
from bs4 import BeautifulSoup
import re
from login import browser

def find_peixun():
    """获取我的专题培训课程url"""

    # https://www.sxgbxx.gov.cn/uc/plan  我的培训
    pei_url = 'https://www.sxgbxx.gov.cn/uc/plan'

    browser.get(pei_url)
    r = browser.page_source
    pei_obj = BeautifulSoup(r, "lxml")
    pei_list = pei_obj.findAll("div", {"class": "e-m-more"})  # 获取我的专题培训内容
    src = './'
    f1 = open(src+'peixun_url.txt', 'w')  # 培训课程的url

    for pid in pei_list:
        pid = str(pid)
        print(pid)
        pid = re.findall(r'id=(.+?)"', pid)
        print(pid)
        peixun_url = 'https://www.sxgbxx.gov.cn/uc/plan/info?id=' + pid[0]  # 生成培训课题的url
        browser.get(peixun_url)

        # print(browser.page_source)
        time.sleep(10)
        r = browser.page_source
        pei_obj = BeautifulSoup(r, "lxml")
        peixun_list = pei_obj.findAll("a", {"class": "lh-reply-btn"})

        for i in peixun_list:
            # print(i)
            # print(i.get_text())
            # print(i['href'])
            i = 'https://www.sxgbxx.gov.cn' + str(i['href'])
            print(i)
            f1.write(i)
            f1.write('\n')

    f1.close()
    print('专题培训url下载成功')


if __name__ == "__main__":
    find_peixun()
    browser.quit()
