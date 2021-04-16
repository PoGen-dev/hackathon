import aiogram

from .Settings import Settings
from .BotTemplate import dispatcher, Template



@dispatcher.message_handler(commands = ['start'])
async def StartCommand(Message: aiogram.types.Message):
    """
    """
    print(1)
    await Template.StartMessage(Message)

