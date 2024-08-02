import re
import json
import time
import random
from collections import OrderedDict
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib import parse
import urllib3

urllib3.disable_warnings()

start = time.time()
first_write = True

past_date_range = datetime.today() - timedelta(days=730)
file_path = 'result_10.txt'
p = re.compile('^(https?://)[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_/.?=]*')

def getSoupData(link):
    url = link
    if p.match(url) != None: 
        res = requests.get(parse.unquote(url), verify=False)
        res.raise_for_status()

        if res.encoding not in ['euc-kr', 'utf-8']:
            res.encoding = 'utf-8'

        soup = BeautifulSoup(res.text, "lxml")
        return soup
    else:
        return None

row_count = 25

page = 1
count = 0
while True:
    target = 'https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_1&page=' + str(page)
    soup = getSoupData(target)
    content_lists = soup.find_all("div", class_="bo_tit")
    #content_dates = soup.find("td", class_="col-date")

    #soup : find로 부터 찾아온 요소에서 텍스트만 추출할때 사용
    #date_time_str = content_dates.string
    #텍스트 날짜 타입으로 변환
    #data_date = datetime.strptime(date_time_str, '%Y.%m.%d.')

    content_links = []
    for i in content_lists:
        aData = i.find('a', href=True)
        #게시글 ID 또는 링크 추출
        content_links.append(aData['href'])
        #content_links.append(aData['boardseqno'])

    #constent_links 에서 하나씩 크롤링하여 콘텐츠 추출 필요
    #main_target = 'https://humanities.snu.ac.kr'
    #main_target = 'https://snucll.snu.ac.kr/board/board_view.php?Mode=I&BoardID=1&page=' + str(page) + '&BoardSeqNo='
    main_target = ''

    input_data = ''
    for i in content_links:
        content_target = main_target + i
        soup_content = getSoupData(content_target)
        print('.', end='')
        if soup_content != None:
            soup_content = soup_content.find('section', id="bo_v_atc")
            input_data += '\n' + i + '||' + soup_content.get_text().replace('\n', '\\n').replace('\r','\\r')
            #json.dumps(data_element, ensure_ascii = False) : json 변환시  ensure_ascii = False 해줘야 한글이 아스키로 변환되지 않음
        else:
            input_data += '\n' +i + '||'
        count += 1

    with open(file_path,'a',encoding='utf-8') as f:
        f.write(input_data)
    f.close()

    page += 1
    print('[' + str(count) + ']')

    if len(content_links) < row_count:
        break

end = time.time()
sec = (end - start)
runningtime = timedelta(seconds=sec)

print(runningtime)
