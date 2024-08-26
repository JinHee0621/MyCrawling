import json
import board_crawl

target_list = open('config/target.json', 'r').readlines()
target_txt = ''.join(target_list)

target_obj = json.loads(target_txt)
print(type(target_obj))
#target_list = json.loads(target_list)
#print(target_list)

#board_crawl.crawl(주소, 목록주소, 게시글 목록테그, 게시글 목록키, 게시글 목록 번호 테그, 게시클 목록 번호,  게시글 접속 주소, 게시글 접속 주소 키, 내용 테그, 내용 키, 게시판 게시글 수, 결과 경로)
#board_crawl.crawl('https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_1&page=', '', 'div', 'bo_tit', 'td','td_num2','a', 'href', 'section', 'bo_v_atc', 25, 'file.txt')