from config import NOTION_TOKEN, DATABASE_ID
from notion_client import Client

notion = Client(auth=NOTION_TOKEN)

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
