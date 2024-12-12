import re
import json
import time
import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib import parse
import urllib3
from collections import OrderedDict

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def convert_date(text): 
    pattern = r'\d{2}\s\D*\s\d{4}'
    date_string = re.findall(pattern, text)[0]

    date_object = datetime.strptime(date_string, '%d %b %Y')
    return date_object.strftime('%Y-%m-%d')

def crawl():
    url = 'https://liberaledu.snu.ac.kr/category/board-206-GN-kuf5d0eK-20231023174836/feed/?var_page=2'
    res = requests.get(parse.unquote(url), headers=headers, verify=False, allow_redirects=True)
    res.raise_for_status()
    if res.encoding not in ['euc-kr', 'utf-8']:
        res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "lxml")
    content_lists = soup.find_all('item')
    #print(soup)
    index = 0
    result_arr = []
    for e in content_lists:
        element = {}
        #링크 수집 default
        link = e.find('a', href=True)
        #print(link['href'])
        element['id_k'] = link['href']

        #링크 comment 
        #link = e.find('comments')
        #print(link.get_text())

        #제목 수집
        #print(link.get_text().strip())
        element['title_ksnu'] = link.get_text().strip()

        #내용 수집
        content = e.find('description')
        #print(content.get_text().strip())
        element['content_ksnu'] = content.get_text().strip()
        
        #link_t
        element['link_t'] = link['href']

        #날짜 수집
        date = e.find('pubdate')
        #print(date.get_text().strip())
        element['date_dt'] = convert_date(date.get_text().strip())
        #print(e)
        result_arr.append(element)
        index += 1

    print(result_arr)
    with open('feed_data.json','a',encoding='utf-8') as f:
        json.dump(result_arr, f, ensure_ascii=False, indent=4)
        #f.write(result_arr)
    f.close()
    #페이지별 글 개수 체크
    print(index)

crawl()

