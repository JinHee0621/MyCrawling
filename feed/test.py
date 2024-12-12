import re
from datetime import datetime

def convert_date(date_string):
    # 날짜 문자열을 datetime 객체로 변환
    date_object = datetime.strptime(date_string, '%d %b %Y')
    
    # 원하는 형식으로 변환하여 반환
    return date_object.strftime('%Y-%m-%d')

text = "Fri, 30 Sep 2024 11:11:39 +0000"
pattern = r'\d{2}\s\D*\s\d{4}'

result = re.findall(pattern, text)
print(result)

result2 = convert_date(result[0])
print(result2)