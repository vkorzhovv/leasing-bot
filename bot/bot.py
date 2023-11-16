from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv()



storage = MemoryStorage()
TOKEN=os.getenv('TOKEN')
admin_id = os.getenv('admin_id')
admin_tg = os.getenv('admin_tg')
domen = os.getenv('domen')
bot = Bot(TOKEN)
dp = Dispatcher(bot,
                storage=storage)
admin_username = os.getenv('admin_username') # юзернейм суперюзера для доступа к API (связь с джанго)
admin_password = os.getenv('admin_password') # пароль суперюзера для доступа к API (связь с джанго)
