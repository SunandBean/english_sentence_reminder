from config import NAVER_ID, NAVER_PW, RECIPIENTS

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

recipients = RECIPIENTS

message = MIMEMultipart()
message['Subject'] = '오늘 날짜 '+'메일 전송 테스트'
message['From'] = f"{NAVER_ID}@naver.com"
message['To'] = ",".join(recipients)

content = """
    <html>
    <body>
        <h1>{title_yesterday}</h1>
        <h2>{date_yesterday}</h2>
        <p>
            메일 전송 테스트입니다
        </p>
        <h1>{title_a_week_ago}</h1>
        <h2>{date_a_week_ago}</h2>
        <p>
            메일 전송 테스트입니다
        </p>
        <h1>{title_a_month_ago}</h1>
        <h2>{date_a_month_ago}</h2>
        <p>
            메일 전송 테스트입니다
        </p>
    </body>
    </html>
""".format(
title_yesterday = '어제 배운 문장',
date_yesterday = '어제 날짜',
title_a_week_ago = '일주일 전에 배운 문장',
date_a_week_ago = '일주일 전 날짜',
title_a_month_ago = '한달 전에 배운 문장',
date_a_month_ago = '한달 전 날짜',
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