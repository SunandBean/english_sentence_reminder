from datetime import datetime, timedelta
import pandas as pd

class Controller:
    def __init__(self, dataframe: pd.DataFrame):
        self.__dataframe = dataframe
        self.__default_address = "https://blog.naver.com/sunandbean"
        self.__start_date = datetime.today()

    def set_start_date(self, start_date: datetime):
        self.__start_date = start_date

    def filter_data(self, num_to_back: int) -> dict:
        target_date = (self.__start_date - timedelta(num_to_back)).date()
        is_target_date = self.__dataframe['date'] == target_date
        df_target_date = self.__dataframe[is_target_date]

        text_target_date = ""
        blog_target_date = ""

        if len(df_target_date) > 0:
            for i in range(len(df_target_date) -1, -1, -1):
                text_target_date += f"<h3>{df_target_date.iloc[i]['eng']}</h3> \
                                    <h4>{df_target_date.iloc[i]['kor']}</h4> <br>"
            blog_target_date = df_target_date.iloc[0]['blog']
        else:
            text_target_date += "<h3>배운 문장이 없습니다! </h3> <br>"
            blog_target_date = self.__default_address
        
        return {"date" : target_date.strftime('%Y-%m-%d'),
                "link" : blog_target_date,
                "text" : text_target_date}