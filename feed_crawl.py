import re
import json
import time
import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib import parse
import urllib3

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = ''
res = requests.get(parse.unquote(url), headers=headers, verify=False, allow_redirects=True)
res.raise_for_status()
if res.encoding not in ['euc-kr', 'utf-8']:
    res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, "lxml")
content_lists = soup.find_all('item')
#print(soup)
index = 0
for e in content_lists:

    #링크 수집 default
    link = e.find('a', href=True)
    print(link['href'])
    #링크 comment 
    #link = e.find('comments')
    #print(link.get_text())

    #제목 수집
    print(link.get_text().strip())

    #날짜 수집
    date = e.find('pubdate')
    print(date.get_text().strip())

    #내용 수집
    content = e.find('description')
    print(content.get_text().strip())

    print()
    print()
    #print(e)

    index += 1

#페이지별 글 개수 체크
print(index)