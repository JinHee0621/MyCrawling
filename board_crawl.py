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

def crawl(url, base_url, board_ele_tag, board_ele_key, board_ele_num_tag, board_ele_num, ele_link_tag, ele_link_key, content_tag, content_key, board_page_count, result_path) : 
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

    urllib3.disable_warnings()
    start = time.time()
    first_write = True
    past_date_range = datetime.today() - timedelta(days=730)

    p = re.compile('^(https?://)[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_/.?=]*')

    row_count = board_page_count
    page = 1
    file_path = result_path
            
    count = 0
    while True:
        target = url + str(page) #'https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_1&page=' + str(page)
        soup = getSoupData(target)
        #게시판의 게시글 목록
        content_lists = soup.find_all(board_ele_tag, class_= board_ele_key)#"div", class_="bo_tit")
        content_numbers = soup.find_all(board_ele_num_tag, class_= board_ele_num)
        #content_dates = soup.find("td", class_="col-date")

        #soup : find로 부터 찾아온 요소에서 텍스트만 추출할때 사용
        #date_time_str = content_dates.string
        #텍스트 날짜 타입으로 변환
        #data_date = datetime.strptime(date_time_str, '%Y.%m.%d.')

        content_links = []
        index = 0
        for i in content_lists:
            ele_num = content_numbers[index].get_text()
            #게시글 ID 또는 링크 추출
            aData = i.find('a', href=True)
            content_links.append(ele_num.strip() + '|' + aData['href'])
            index += 1
            #content_links.append(aData['boardseqno'])

        #constent_links 에서 하나씩 크롤링하여 콘텐츠 추출 필요
        #main_target = 'https://humanities.snu.ac.kr'
        #main_target = 'https://snucll.snu.ac.kr/board/board_view.php?Mode=I&BoardID=1&page=' + str(page) + '&BoardSeqNo='
        main_target = base_url
        input_data = ''

        for i in content_links:
            link_ele = i.split('|')
            link_num = link_ele[0]
            link_url = link_ele[1]
            print(link_num + ' ' + link_url)

            if link_num.isdigit():
                content_target = main_target + link_url
                soup_content = getSoupData(content_target)
                print('.', end='')
                if soup_content != None:
                    soup_content = soup_content.find(content_tag, id=content_key)#'section', id="bo_v_atc")
                    input_data += '\n' + link_url + '||' + soup_content.get_text().replace('\n', '\\n').replace('\r','\\r')
                    #json.dumps(data_element, ensure_ascii = False) : json 변환시  ensure_ascii = False 해줘야 한글이 아스키로 변환되지 않음
                else:
                    input_data += '\n' +link_url + '||'
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
