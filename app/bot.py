import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyrogram import Client as PyroClient
# === Локальные модули ===

load_dotenv('app/.env')

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
TOKEN = os.getenv('TOKEN')
BOT_LINK = os.getenv('BOT_LINK')
DEV = os.getenv('DEV')

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot,storage=storage)
app = PyroClient("BlackDuke_bot", api_id=API_ID, api_hash=API_HASH)

logging.basicConfig(
    filename='app/logs/bot.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)