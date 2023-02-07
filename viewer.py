import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime

class Viewer:
    def __init__(self, naver_id: str, naver_pw: str, customers: list[str]):
        self.__mail_id = naver_id
        self.__mail_pw = naver_pw
        self.__customers = customers

        self.__contents = []

    def add_content(self, content: dict):
        self.__contents.append(content)

    def send_mail(self):
        message = MIMEMultipart()
        message['Subject'] = f"[{datetime.today().strftime('%Y-%m-%d')}] 영어 문장 리마인더"
        message['From'] = f"{self.__mail_id}@naver.com"
        message['Bcc'] = ",".join(self.__customers)

        content_start = """
            <html>
            <body>
        """

        content_body = ""
        if len(self.__contents) > 0:
            for content in self.__contents:
                content_body += f"""
                    <a href={content['link']} target = "_blank"> <h2>{content['date']} 에 배운 문장</h2> </a>
                    <ul>
                        {content['text']}
                    </ul>
                    <hr>
                """
        else:
            content_body = f"""
                <a href="https://blog.naver.com/sunandbean" target = "_blank"> <h2>공유할 문장이 없습니다! </h2> </a>
                <hr>
            """

        content_end = """
            </body>
            </html>
        """
        
        content_total = content_start + content_body + content_end
        mimetext = MIMEText(content_total,'html')
        message.attach(mimetext)

        server = smtplib.SMTP('smtp.naver.com',587)
        server.ehlo()
        server.starttls()
        server.login(self.__mail_id,self.__mail_pw)
        server.sendmail(message['From'], self.__customers, message.as_string())
        server.quit()
