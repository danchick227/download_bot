from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN= os.environ['BOT_TOKEN']

if not BOT_TOKEN:
    raise ValueError("токен пустой")