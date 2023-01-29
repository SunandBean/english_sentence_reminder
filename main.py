from config import NOTION_TOKEN, DATABASE_ID
from model import Model

if __name__ == "__main__":
    model = Model(NOTION_TOKEN, DATABASE_ID)
