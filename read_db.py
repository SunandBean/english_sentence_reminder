from config import NOTION_TOKEN, DATABASE_ID
from notion_client import Client
from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd

notion = Client(auth=NOTION_TOKEN)

# query data from notion
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

# filter data
today = datetime.today().date()

yesterday = (datetime.today() - timedelta(1)).date()
is_yesterday = df['date'] == yesterday
df_yesterday = df[is_yesterday]

print("어제 배운 문장 (" + yesterday.strftime('%Y-%m-%d') +")")
if len(df_yesterday) > 0:
    data_yesterday = {}
    for i in range(len(df_yesterday)-1, -1, -1):
        print("- 영어: " + df_yesterday.iloc[i]['eng'])
        print("- 해석: " + df_yesterday.iloc[i]['kor'])
        print("- 블로그: " + df_yesterday.iloc[i]['blog'])
        print("- 유튜브: " + df_yesterday.iloc[i]['youtube'])
        print()
else:
    print("- 배운 문장이 없습니다!")
    print()


a_week_ago = (datetime.today() - timedelta(7)).date()
is_a_week_ago = df['date'] == a_week_ago
df_a_week_ago = df[is_a_week_ago]

print("일주일 전에 배운 문장 (" + a_week_ago.strftime('%Y-%m-%d') +")")
if len(df_a_week_ago) > 0:
    data_a_week_ago = {}
    for i in range(len(df_a_week_ago)-1, -1, -1):
        print("- 영어: " + df_a_week_ago.iloc[i]['eng'])
        print("- 해석: " + df_a_week_ago.iloc[i]['kor'])
        print("- 블로그: " + df_a_week_ago.iloc[i]['blog'])
        print("- 유튜브: " + df_a_week_ago.iloc[i]['youtube'])
        print()
else:
    print("- 배운 문장이 없습니다!")
    print()
    

a_month_ago = (datetime.today() - timedelta(30)).date()
is_a_month_ago = df['date'] == a_month_ago
df_a_month_ago = df[is_a_month_ago]
print("한달 전에 배운 문장 (" + a_month_ago.strftime('%Y-%m-%d') +")")

if len(df_a_month_ago) > 0:
    data_a_month_ago = {}
    for i in range(len(df_a_month_ago)-1, -1, -1):
        print("- 영어: " + df_a_month_ago.iloc[i]['eng'])
        print("- 해석: " + df_a_month_ago.iloc[i]['kor'])
        print("- 블로그: " + df_a_month_ago.iloc[i]['blog'])
        print("- 유튜브: " + df_a_month_ago.iloc[i]['youtube'])
        print()
else:
    print("- 배운 문장이 없습니다!")
    print()

    
# 모델 설계
