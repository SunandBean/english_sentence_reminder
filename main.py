from config import NOTION_TOKEN, DATABASE_ID
from model import Model
from controller import Controller

if __name__ == "__main__":
    model = Model(NOTION_TOKEN, DATABASE_ID)
    controller = Controller(model.get_dataframe())
    
