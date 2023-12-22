import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="timmy"
)

def convert_relative_time(relative_time):
    # 获取当前日期和时间
    now = datetime.now()

    # 使用正则表达式提取数值和单位
    match = re.match(r"(\d+)(\D+)", relative_time)
    if match:
        value = int(match.group(1))
        unit = match.group(2)

        # 根据单位计算时间间隔
        if unit == "周前":
            delta = timedelta(days=value * 7)
        elif unit == "年前":
            delta = timedelta(days=value * 365)
        elif unit == "个月前":
            delta = timedelta(days=value * 30)
        elif unit == "天前":
            delta = timedelta(days=value)
        else:
            print(unit)
            raise ValueError(unit)


        # 计算真实日期
        real_date = now - delta

        return real_date
    else:
        raise ValueError("无效的相对时间格式")
def scraping_page(url):
        driver.get(url)

        old_div_lens = 0
        while 1:
            # 下滑刷新数据到无法下滑
            actions = ActionChains(driver)
            actions.send_keys(Keys.END)  # 模拟按下 "END" 键
            actions.perform()

            time.sleep(1)

            # 获取页面的视频数量
            # ytd-rich-grid-row标签

            div_list = driver.find_elements(By.XPATH, '//div[@id="contents"]/ytd-rich-item-renderer')

            # 比较视频数量，如果没变化就跳出循环
            if len(div_list) == old_div_lens:
                break
            else:
                old_div_lens = len(div_list)
            # break
        # 拿页面数据

        div_list = driver.find_elements(By.XPATH, '//div[@id="contents"]/ytd-rich-item-renderer')
        data_list = []
        author = driver.find_element(By.XPATH, '//*[@id="text"]').text
        for div in div_list:
            href = div.find_element(By.XPATH, './div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a').get_attribute(
                'href')
            title = div.find_element(By.XPATH,
                                     './div/ytd-rich-grid-media/div[1]/div[3]/div[1]/h3/a/yt-formatted-string').text
            views_number = div.find_element(By.XPATH,
                                            './div/ytd-rich-grid-media/div[1]/div[3]/div[1]/ytd-video-meta-block/div[1]/div[2]/span[1]').text


            #处理观看数字
            views_number = views_number.replace('次观看','').replace('万','000').replace('.','')
            post_time = div.find_element(By.XPATH,
                                         './div/ytd-rich-grid-media/div[1]/div[3]/div[1]/ytd-video-meta-block/div[1]/div[2]/span[2]').text

            post_time = convert_relative_time(post_time)
            print(post_time)
            try:
                img_src = div.find_element(By.XPATH,
                                           './div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a/yt-image/img').get_attribute(
                    'src').split('?')[0]
            except:
                img_src = div.find_element(By.XPATH,
                                           './div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a/yt-image/img').get_attribute(
                    'src')
            data_list.append(
                [title, views_number, post_time, href, img_src,author]
            )

        # # 保存数据 到 excel
        # df = pd.DataFrame(data_list)
        # df.to_excel('data.xlsx', index=False)
        #
        # driver.quit()

        # 保存数据到mysql

        cursor = mydb.cursor()

        mysql = "insert into app001_youtube(title,views_number,post_time,href,img_src,author) values(%s,%s,%s,%s,%s,%s)"

        cursor.executemany(mysql, data_list)

        print(url,cursor.rowcount, "rows")

        mydb.commit()

if __name__ == '__main__':

    urls = ['https://www.youtube.com/@Necrize_/videos','https://www.youtube.com/@Hcpeful/videos','https://www.youtube.com/@WhoKoa/videos','https://www.youtube.com/@Ozhiy']

    driver = webdriver.Edge()

    for url in urls:
        scraping_page(url)


