import aiogram
from aiogram.contrib.fsm_storage import memory

from .Settings import Settings


bot = aiogram.Bot(token=Settings.TOKEN)
dispatcher = aiogram.Dispatcher(bot, storage = memory.MemoryStorage())

class Template: 

    async def StartMessage(Message: aiogram.types.Message) -> None: 
        """
        """
        print(1)
        await bot.send_message(Message.chat.id, 'Hello')

