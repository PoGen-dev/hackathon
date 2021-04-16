import aiogram

from .BotTemplate import bot, Template

class Activity: 

    async def StartMessage(Message: aiogram.types.Message) -> None: 
        """
        """
        await bot.send_message(Message.chat.id, 'Hello')