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
text_yesterday = ""
if len(df_yesterday) > 0:
    data_yesterday = {}
    for i in range(len(df_yesterday)-1, -1, -1):
        print("- 영어: " + df_yesterday.iloc[i]['eng'])
        print("- 해석: " + df_yesterday.iloc[i]['kor'])
        print("- 블로그: " + df_yesterday.iloc[i]['blog'])
        print("- 유튜브: " + df_yesterday.iloc[i]['youtube'])
        print()
        text_yesterday += f"- 영어: {df_yesterday.iloc[i]['eng']}\n - 해석: {df_yesterday.iloc[i]['kor']}\n - 블로그: {df_yesterday.iloc[i]['blog']}\n - 유튜브: {df_yesterday.iloc[i]['youtube']}\n\n"
else:
    print("- 배운 문장이 없습니다!")
    print()
    text_yesterday += "- 배운 문장이 없습니다!\n"


a_week_ago = (datetime.today() - timedelta(7)).date()
is_a_week_ago = df['date'] == a_week_ago
df_a_week_ago = df[is_a_week_ago]
print("일주일 전에 배운 문장 (" + a_week_ago.strftime('%Y-%m-%d') +")")
text_a_week_ago = ""
if len(df_a_week_ago) > 0:
    data_a_week_ago = {}
    for i in range(len(df_a_week_ago)-1, -1, -1):
        print("- 영어: " + df_a_week_ago.iloc[i]['eng'])
        print("- 해석: " + df_a_week_ago.iloc[i]['kor'])
        print("- 블로그: " + df_a_week_ago.iloc[i]['blog'])
        print("- 유튜브: " + df_a_week_ago.iloc[i]['youtube'])
        print()
        text_a_week_ago += f"- 영어: {df_a_week_ago.iloc[i]['eng']}\ - 해석: {df_a_week_ago.iloc[i]['kor']}\n - 블로그: {df_a_week_ago.iloc[i]['blog']}\n - 유튜브: {df_a_week_ago.iloc[i]['youtube']}\n\n"

else:
    print("- 배운 문장이 없습니다!")
    print()
    text_a_week_ago += "- 배운 문장이 없습니다!\n"
    

a_month_ago = (datetime.today() - timedelta(30)).date()
is_a_month_ago = df['date'] == a_month_ago
df_a_month_ago = df[is_a_month_ago]
print("한달 전에 배운 문장 (" + a_month_ago.strftime('%Y-%m-%d') +")")
text_a_month_ago = ""
if len(df_a_month_ago) > 0:
    data_a_month_ago = {}
    for i in range(len(df_a_month_ago)-1, -1, -1):
        print("- 영어: " + df_a_month_ago.iloc[i]['eng'])
        print("- 해석: " + df_a_month_ago.iloc[i]['kor'])
        print("- 블로그: " + df_a_month_ago.iloc[i]['blog'])
        print("- 유튜브: " + df_a_month_ago.iloc[i]['youtube'])
        print()
        text_a_month_ago += f"<h3>{df_a_month_ago.iloc[i]['eng']}</h3> \
                            <h4>{df_a_month_ago.iloc[i]['kor']}</h4> <br>"

else:
    print("- 배운 문장이 없습니다!")
    print()
    text_a_month_ago += "- 배운 문장이 없습니다!\n"


from config import NAVER_ID, NAVER_PW, RECIPIENTS

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

recipients = RECIPIENTS

message = MIMEMultipart()
message['Subject'] = f"{today.strftime('%Y-%m-%d')} 메일 전송 테스트"
message['From'] = f"{NAVER_ID}@naver.com"
message['To'] = ",".join(recipients)

content = """
    <html>
    <body>
        <a href={link_yesterday} target = "_blank"> <h1>{title_yesterday}</h1> </a>
        <ul>
            {content_yesterday}
        </ul>
        <hr>
        <a href={link_a_week_ago} target = "_blank"> <h1>{title_a_week_ago}</h1> </a>
        <ul>
            {content_a_week_ago}
        </ul>
        <hr>
        <a href={link_a_month_ago} target = "_blank"> <h1>{title_a_month_ago}</h1> </a>
        <h2>{date_a_month_ago}</h2>
        <ul>
            {content_a_month_ago}
        </ul>
    </body>
    </html>
""".format(
link_yesterday = df_yesterday.iloc[0]['blog'],
title_yesterday = f"어제({yesterday.strftime('%Y-%m-%d')}) 배운 문장",
content_yesterday = text_yesterday,

link_a_week_ago = df_yesterday.iloc[0]['blog'],
title_a_week_ago = f"일주일 전({a_week_ago.strftime('%Y-%m-%d')})에 배운 문장",
content_a_week_ago = text_a_week_ago,

link_a_month_ago = df_yesterday.iloc[0]['blog'],
title_a_month_ago = '한달 전에 배운 문장',
content_a_month_ago = text_a_month_ago,
)

mimetext = MIMEText(content,'html')
message.attach(mimetext)

email_id = NAVER_ID
email_pw = NAVER_PW

server = smtplib.SMTP('smtp.naver.com',587)
server.ehlo()
server.starttls()
server.login(email_id,email_pw)
server.sendmail(message['From'],recipients,message.as_string())
server.quit()