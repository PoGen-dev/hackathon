import aiogram

from .BotTemplate import bot

class Activity: 

    async def StartMessage(Message: aiogram.types.Message) -> None: 
        """
        """
        print(1)
        await bot.send_message(Message.chat.id, 'Hello')