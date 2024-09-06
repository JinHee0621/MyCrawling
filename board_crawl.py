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


def crawl(url, base_url, board_ele_tag, board_ele_key, board_ele_num_tag, board_ele_num, ele_url, ele_url_key, 
ele_date_tag, ele_date_key, content_tag, content_key_type, content_key, result_path) : 
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
            res = requests.get(parse.unquote(url), verify=False)
            res.raise_for_status()

            if res.encoding not in ['euc-kr', 'utf-8']:
                res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "lxml")
            return soup

    urllib3.disable_warnings()
    start = time.time()
    first_write = True
    past_date_range = datetime.today() - timedelta(days=730)

    p = re.compile('^(https?://)[a-zA-Z0-9-\\:.?=]+\\.[a-zA-Z0-9-.?=]+/[a-zA-Z0-9-_/.?=]*')

    #row_count = int(board_page_count)
    page = 1
    file_path = result_path
            
    count = 0
    while True:
        target = url + str(page) #'https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_1&page=' + str(page)
        soup = getSoupData(target)
        #게시판의 게시글 목록
        content_lists = soup.find_all(board_ele_tag, class_= board_ele_key)
        content_numbers = soup.find_all(board_ele_num_tag, class_= board_ele_num)
        content_dates = soup.find_all(ele_date_tag, class_=ele_date_key)

        #soup : find로 부터 찾아온 요소에서 텍스트만 추출할때 사용
        #date_time_str = content_dates.string
        #텍스트 날짜 타입으로 변환
        #data_date = datetime.strptime(date_time_str, '%Y.%m.%d.')
        content_links = []
        index = 0
        for num in content_numbers:
            #게시글제목
            ele_num = ''
            ele_num = num.get_text().strip()
            if ele_num.isdigit():
                i = content_lists[index]
                #게시일자
                ele_date = ''
                ele_date = content_dates[index].get_text()
                
                ele_title = ''
                for link_ele in i.find_all(ele_url):
                    # 제목에 내용 링크가 있으며 제목의 길이는 6자 이상인것 기준으로 링크를 가져옴
                    if len(link_ele.get_text()) > 6:
                        aData = link_ele
                        ele_title = link_ele.get_text()

                #게시글 ID 또는 링크 추출
                #aData = i.find('a', href=True)
                content_links.append(ele_num.strip() + '|' + aData['href'] + '|' + ele_title +  '|' + ele_date)
                index += 1

        #constent_links 에서 하나씩 크롤링하여 콘텐츠 추출 필요
        #게시글 별 링크의 상위 링크 존재 여부에 따라 필요한 base_url : 예) 게시글별 링크에 저장된 값 : /bbs/123 -> www.snu.com/bbs/123 으로 나올수 있도록 필요한 www.snu.com
        main_target = base_url
        input_data = ''
        for i in content_links:    
            link_ele = i.split('|')
            link_num = link_ele[0]
            link_url = link_ele[1]
            link_title = link_ele[2].strip()
            link_date = link_ele[3]
            #print(link_num + ' ' + link_url)
            if link_num.isdigit():
                content_target = main_target + link_url
                soup_content = getSoupData(content_target)
                #print(content_target)
                #print(soup_content)
                print('.', end='')
                if soup_content != None:
                    if content_key_type == 'class':
                        soup_content = soup_content.find(content_tag, class_=content_key)#'section', id="bo_v_atc")
                    elif content_key_type == 'id':
                        soup_content = soup_content.find(content_tag, id=content_key)

                    input_data += '\n' + content_target + '||'+ link_title + '||' + link_date + '||' + soup_content.get_text().replace('\n', '\\n').replace('\r','\\r') 
                    #json.dumps(data_element, ensure_ascii = False) : json 변환시  ensure_ascii = False 해줘야 한글이 아스키로 변환되지 않음
                else:
                    input_data += '\n' +content_target + '||'+ link_title + '||' + link_date + '||'
                count += 1

        with open(file_path,'a',encoding='utf-8') as f:
            f.write(input_data)
        f.close()

        page += 1
        print('[' + str(count) + ']')

        #테스트: 수집 데이터 개수 20개 이상일때 다음으로
        if count >= 20:
            break

        #if len(content_links) < row_count:
            #break

    end = time.time()
    sec = (end - start)
    runningtime = timedelta(seconds=sec)

    print(runningtime)
