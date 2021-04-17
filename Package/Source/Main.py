import aiogram

from .Settings import RegistrationState, Settings
from .BotTemplate import dispatcher
from .BotActivity import Activity


class TelegramBot:
    
#   COMMANDS

    @dispatcher.message_handler(commands = ['start'])
    async def StartCommand(Message: aiogram.types.Message):
        """
        """
        await Activity.StartMessage(Message)

    @dispatcher.message_handler(commands = ['help'])
    async def HelpCommand(Message: aiogram.types.Message):
        """
        """
        await Activity.HelpMessage(Message)
    
    @dispatcher.message_handler(commands = ['status'])
    async def StatusCommand(Message: aiogram.types.Message):
        """
        """
        await Activity.StatusMessage(Message)

    @dispatcher.message_handler(commands = ['rule'])
    async def RuleCommand(Message: aiogram.types.Message):
        """
        """
        await Activity.RuleMessage(Message)

#   CONTENT TYPES

    @dispatcher.message_handler(content_types=['text'])
    async def message_reply(Message: aiogram.types.Message):
        """
        """
        await Activity.ReplyMessage(Message)

    @dispatcher.message_handler(content_types = ['document'])
    async def take_file(Message: aiogram.types.Message):
        """
        """
        await Activity.GetDocument(Message)

#   STATE

    @dispatcher.message_handler(state = RegistrationState.DocIndex)
    async def EnterDocIndex(Message: aiogram.types.Message):
        """
        """
        await Activity.ReactionOnState(Message)

















