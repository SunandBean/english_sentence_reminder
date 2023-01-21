from config import NOTION_TOKEN
import notion_client as Client

notion = Client(auth=NOTION_TOKEN)