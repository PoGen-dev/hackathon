import aiogram

from .Settings import Settings
from .BotTemplate import dispatcher
from .BotActivity import Activity


class TelegramBot:
    
    @dispatcher.message_handler(commands = ['start'])
    async def StartCommand(Message: aiogram.types.Message):
        """
        """
        await Activity.StartMessage(Message)