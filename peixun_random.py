from login import browser
from bs4 import BeautifulSoup
from login import start_time
import time,re,random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

src = './'

def peixun_random():
    """专题培训学习"""
    print('专题学习')
    with open(src+'peixun_url.txt', 'r') as f:
        cou_url_list = f.read().splitlines()

        sum = len(cou_url_list)

    for x in range(1, 100):  # 每次随机学习，学习100次

        # 培训页面
        pei_url = (cou_url_list[random.randint(1, sum - 1)])
        # for pei_url in cou_url_list:
        try:
            browser.get(pei_url)
            print('--------------------------------------')
            print(pei_url)
            # print(browser.page_source)

            browser.find_element_by_xpath(
                '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li').click()  # 切换到培训内容详情页

            # print(browser.page_source)
            cou_obj = BeautifulSoup(browser.page_source, 'lxml')
            time.sleep(3)
            li_list = cou_obj.findAll('li')  # 找到所有培训课程
            # print('--------------------------------------')
            # print(li_list)
        except TimeoutException:
            print('加载时间异常')
            continue
        except NoSuchElementException:
            print('加载元素异常')
            continue
        except WebDriverException:
            print('webdriver异常')
            continue
        
        for li in li_list:
            try:
                end_time = time.time()
                study_time = (end_time - start_time) / 60   # 以分为单位
                study_time = int(study_time)                # 取整
                dtime = int(study_time / 60 / 24)           # 天
                other = study_time % (24*60) 
                htime = other // 60                         # 时
                mtime = other % 60                          # 分
                
                print('已学习%s天%s时%s分' % (dtime,htime,mtime))

                li_html = str(li)
                # print('--------------------------------------')
                # print(li_html)
                if 'kpoint_list' not in li_html:
                    continue
                id = re.findall(r'kp_\d+', li_html)
                id = ''.join(id)
                print(id)
            
                if '视频播放' in li_html:
                    if '100%' in li_html:
                        continue
                    title = li.get_text()  # 找到课程标题
                    print(title)
                    shichang = re.findall(r'\d+分\d+秒', li_html)
                    shichang = re.findall(r'\d+', str(shichang))
                    shichang = int(shichang[0]) * 60 + int(shichang[1])
                    percent = re.findall(r'\d+\%', li_html)
                    percent = re.findall(r'\d+', str(percent))
                    percent = int(percent[0])
                    print('看视频')
                    print("本视频长%s秒" % shichang)
                    print("已学习%d%%" % percent)
                    t = shichang * (100 - percent) * 0.01
                    browser.find_element_by_id(id).click()
                    time.sleep(3)
                    action = ActionChains(browser)
                    # title = browser.find_element_by_xpath('//*[@id="N-course-box"]/article/div/div[2]/section/h3/span')  # 鼠标移动到标题
                    # action.move_to_element(title).click().perform()
                    time.sleep(20)
                    action.send_keys(Keys.SPACE).perform()  # 单击空格
                    time.sleep(t + 40)
                    print(li.get_text() + "学习完毕")
                    print('\n')
                    print('\n')
                    browser.refresh()

                elif '音频播放' in li_html:
                    if '100%' in li_html:
                        continue
                    title = li.get_text()  # 找到课程标题
                    print(title)
                    shichang = re.findall(r'\d+分\d+秒', li_html)
                    shichang = re.findall(r'\d+', str(shichang))
                    shichang = int(shichang[0]) * 60 + int(shichang[1])
                    percent = re.findall(r'\d+\%', li_html)
                    percent = re.findall(r'\d+', str(percent))
                    percent = int(percent[0])
                    print('听音频')
                    print("本音频长%s秒" % shichang)
                    print("已学习%d%%" % percent)
                    t = shichang * (100 - percent) * 0.01
                    browser.find_element_by_id('yp_play').click()
                    time.sleep(t + 20)
                    print(li.get_text() + "学习完毕")
                    print('\n')
                    print('\n')
                    browser.refresh()

                elif '随堂小测验' in li_html:
                    continue

                else:
                    print('读文字')
                    browser.find_element_by_id(id).click()
                    time.sleep(5)
                    print(li.get_text() + "学习完毕")
                    print('\n')
                    print('\n')
                    browser.refresh()
            except TimeoutException:
                print('加载时间异常')
                continue
            except NoSuchElementException:
                print('加载元素异常')
                continue
            except WebDriverException:
                print('webdriver异常')
                continue
