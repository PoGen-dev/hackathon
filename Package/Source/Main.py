import aiogram

from .Settings import RegistrationState, Settings
from .BotTemplate import Template, dispatcher
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
    async def EnterDocIndex(Message: aiogram.types.Message, state: aiogram.dispatcher.storage.FSMContext):
        """
        """
        await Activity.ReactionOnState(Message, state)

#   CALLBACK QUERY

    @dispatcher.callback_query_handler(lambda Message: True)
    async def ProcessCallbackQuery(CallbackQuery: aiogram.types.callback_query.CallbackQuery):
        """
        """
        Code = int(CallbackQuery.data)
        ActivityDict = {
            'FileSystem': Template.SendDocument
            }
        Func = ActivityDict.get(Settings.Keyboard[Code][1])
        await Func(CallbackQuery)












