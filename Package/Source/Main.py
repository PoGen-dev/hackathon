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

    @dispatcher.message_handler(content_types = ['document'])
    async def take_file(Message: aiogram.types.Message):
        """
        """
        await Activity.GetDocument(Message)

        

















