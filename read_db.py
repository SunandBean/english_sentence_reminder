from config import NOTION_TOKEN, DATABASE_ID
from notion_client import Client
from datetime import datetime
from pprint import pprint

import pandas as pd

notion = Client(auth=NOTION_TOKEN)

data = notion.databases.query(DATABASE_ID)
database_object = data['object']
has_more = data['has_more']
next_cursor = data['next_cursor']
while has_more:
    data_while = notion.databases.query(DATABASE_ID, start_cursor=next_cursor)
    for row in data_while['results']:
        data['results'].append(row)
    has_more = data_while['has_more']
    next_cursor = data_while['next_cursor']


# # Check data
# for result in data['results']:
#     for key, value in result['properties'].items():
#         print("key: ", key)
#         if value['type'] == 'date':
#             print("value: " + value['date']['start'])
#         elif value['type'] == 'url':
#             print("value: " + value['url'])
#         elif value['type'] == 'rich_text':
#             print("value: " + value['rich_text'][0]['plain_text'])
#         elif value['type'] == 'title':
#             print("value: " + value['title'][0]['plain_text'])
#         else:
#             print("useless type")

# arrange data
arranged_data = []
for result in data['results']:
    chunk = {}
    for key, value in result['properties'].items():
        if key == "영어 문장":
            chunk['eng'] = value['title'][0]['plain_text']
        elif key == "한글 해석":
            chunk['kor'] = value['rich_text'][0]['plain_text']
        elif key == "포스팅 링크":
            chunk['blog'] = value['url']
        elif key == "영상 링크":
            chunk['youtube'] = value['url']
        elif key == "공부한 날":
            date_time_str = value['date']['start']
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d').date()
            chunk['date'] = date_time_obj
    arranged_data.append(chunk)

df = pd.DataFrame(arranged_data)
print(df)

# 모델 설계
