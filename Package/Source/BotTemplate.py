import aiogram
from aiogram.contrib.fsm_storage import memory

from .Settings import Settings


bot = aiogram.Bot(token=Settings.TOKEN)
dispatcher = aiogram.Dispatcher(bot, storage = memory.MemoryStorage())

class Template: 

    pass

