from config import NOTION_TOKEN, DATABASE_ID, NAVER_ID, NAVER_PW, CUSTOMERS, GSPREAD_KEY, GSPREAD_SHEET_URL, GSPREAD_SHEET_NAME, MAIL_COL_NUM
from model import Model
from controller import Controller
from viewer import Viewer

import os
import gspread

if __name__ == "__main__":
    model = Model(NOTION_TOKEN, DATABASE_ID)
    controller = Controller(model.get_dataframe())

    if os.path.isfile(GSPREAD_KEY):
        gc = gspread.service_account(filename=GSPREAD_KEY)
        spread_sheet = gc.open_by_url(GSPREAD_SHEET_URL)
        mail_sheet = spread_sheet.worksheet(GSPREAD_SHEET_NAME)
        mail_list = mail_sheet.col_values(MAIL_COL_NUM)
        CUSTOMERS = mail_list

    viewer = Viewer(NAVER_ID, NAVER_PW, CUSTOMERS)

    viewer.add_content(controller.filter_data(1)) # yesterday
    viewer.add_content(controller.filter_data(7)) # a week ago
    viewer.add_content(controller.filter_data(30)) # a month ago

    viewer.send_mail()

