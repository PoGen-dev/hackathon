import aiogram
from aiogram.contrib.fsm_storage import memory

from .Settings import Settings


bot = aiogram.Bot(token=Settings.TOKEN)
print(1)
dispatcher = aiogram.Dispatcher(bot, storage = memory.MemoryStorage())
print(2)
class Template: 

    pass

