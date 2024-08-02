#동적페이지 크롤링 Selenium & BeautifulSoup
import re
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib import parse
import urllib3
urllib3.disable_warnings()
start = time.time()
file_path = 'result_7.txt'

#Selenium Chrome 실행 옵션 : Chrome 실행 창을 띄우지 않도록 
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

page = 1
default_size = 20


while True:
    url = 'https://korean.snu.ac.kr/category/board_3_gn_44wycjtw_20201202131822/?var_page=' + str(page)
    #게시글페이지 이동
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'lxml')
    #게시글페이지에서 게시글 목록 get
    content_lists = soup.find_all("div", class_="subject")
    title_list = []

    for i in content_lists:
        #게시글 제목찾기
        title_list.append(i.find("strong").text.strip())

    title_index = 0

    while title_index < len(title_list):
        title_ele = title_list[title_index]

        try:         
            element_by_link_text = driver.find_element(By.LINK_TEXT, title_ele)
            #페이지 이동
            element_by_link_text.click()
            next_soup = BeautifulSoup(driver.page_source,'lxml')
            content = next_soup.find('div', class_='board_view_content')
            input_data = '\n' + title_ele + '||' + content.get_text().replace('\n', '\\n').replace('\r','\\r')

        except Exception as e:
            input_data = '\n' + title_ele + '||' + str(e).replace('\n', '\\n').replace('\r','\\r')
            pass

        with open(file_path,'a',encoding='utf-8') as f:
            f.write(input_data)
        f.close()

        driver.back()
        title_index += 1


    if len(title_list) != default_size:
        break
    else:
        page += 1


end = time.time()
sec = (end - start)
runningtime = datetime.timedelta(seconds=sec)
print(runningtime)