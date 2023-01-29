from config import NOTION_TOKEN, DATABASE_ID, NAVER_ID, NAVER_PW, CUSTOMERS
from model import Model
from controller import Controller
from viewer import Viewer

if __name__ == "__main__":
    model = Model(NOTION_TOKEN, DATABASE_ID)
    controller = Controller(model.get_dataframe())
    viewer = Viewer(NAVER_ID, NAVER_PW, CUSTOMERS)

    viewer.add_content(controller.filter_data(1)) # yesterday
    viewer.add_content(controller.filter_data(7)) # a week ago
    viewer.add_content(controller.filter_data(30)) # a month ago

    viewer.send_mail()

