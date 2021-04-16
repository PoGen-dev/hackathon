import aiogram

from .Settings import Settings
from .BotTemplate import dispatcher
from .BotActivity import Activity


class TelegramBot:
    
    print(1)
    @dispatcher.message_handler(commands = ['start'])
    async def StartCommand(Message: aiogram.types.Message):
        """
        """
        print(1)
        await Activity.StartMessage(Message)