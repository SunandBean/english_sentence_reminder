from notion_client import Client
from datetime import datetime

import pandas as pd

class Model:
    def __init__(self, notion_token, database_id):
        self._notion_client = Client(auth=notion_token)
        self._database_id = database_id

        self.__query()
        self.__arrange()
    
    def __query(self):
        # query data from notion
        data = self._notion_client.databases.query(self._database_id)
        has_more = data['has_more']
        next_cursor = data['next_cursor']
        while has_more:
            data_while = self._notion_client.databases.query(self._database_id, start_cursor=next_cursor)
            for row in data_while['results']:
                data['results'].append(row)
            has_more = data_while['has_more']
            next_cursor = data_while['next_cursor']
        self.__data = data["results"]

    def __arrange(self):
        arranged_data = []
        for result in self.__data['results']:
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

        self.__dataframe = pd.DataFrame(arranged_data)

    def get_dataframe(self):
        return self.__dataframe
