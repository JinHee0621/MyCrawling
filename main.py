import json
import board_crawl

target_list = open('config/target.json', 'r', encoding='UTF8').readlines()
target_txt = ''.join(target_list)

target_obj = json.loads(target_txt) # 타겟 목록 파일 내용 가져오기

#target = target_obj[0]
#board_crawl.crawl(target['url'], target['list_url'], target['list_tag'], target['list_key'], target['list_num_tag'], target['list_num_key'], target['ele_url'], target['ele_url_key'],
#target['ele_date_tag'], target['ele_date_key'], target['content_tag'], target['content_key_type'], target['content_key'], target['row_count'], target['dest'])

for target in target_obj:
    print(target['name'])
    if target['name'].find('err') > -1:
        continue
    else:
        board_crawl.crawl(target['url'], target['list_url'], target['list_tag'], target['list_key'], target['list_num_tag'], target['list_num_key'], target['ele_url'], target['ele_url_key'], target['ele_date_tag'], target['ele_date_key'], target['content_tag'], target['content_key_type'], target['content_key'], target['dest'], target['board_size'])

#target_list = json.loads(target_list)
#print(target_list)

#board_crawl.crawl(주소, 목록주소, 게시글 목록테그, 게시글 목록키, 게시글 목록 번호 테그, 게시클 목록 번호 키,  게시글 접속 주소테그, 게시글 접속 주소 키, 내용 테그, 내용 키, 게시판 게시글 수, 결과 경로)
#board_crawl.crawl('https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_1&page=', '', 'div', 'bo_tit', 'td','td_num2','a', 'href', 'section', 'bo_v_atc', 25, 'file.txt')