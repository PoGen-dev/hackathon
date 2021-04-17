import aiogram

from .BotTemplate import bot, Template
from .Settings import RegistrationState, Settings
from .BotChecks import Checks

class Activity: 

    async def StartMessage(Message: aiogram.types.Message) -> None: 
        """
        Reaction on '/start'. 

        1. Preparation basic info
        2. Create default structure in FileSystem
        3. Bot send message

        :param aiogram.types.Message Message:
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message)
        #   Create default structure in FileSystem
        Template.CreateDefaultFileSystem(Info.get('UserID'))
        #   Bot send message
        await bot.send_message(Info.get('UserID'), 'Добро пожаловать.\nЯ помогу ' +
            'тебе составить отчёт, для этого тебе нужно всего лишь отправить мне ' +
            'файл в формате .frx или .fpx.\nИспользуй /help, чтобы узнать ' + 
            'подробности взаимодействия со мной и мои возможности.',
            reply_markup = Template.CreateKeyboardByInsert(
                Template.UniteKeyboardBySubgroup(
                    'AdditionalOptions', Settings.Keyboard.copy()), 
                'Reply'))
    
    async def HelpMessage(Message: aiogram.types.Message) -> None: 
        """
        Reaction to command '/status'.

        :param aiogram.types.Message Message: 
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message)
        #   Bot send message 
        await bot.send_message(Info.get('UserID'), 
            'Краткое описание команд:\n\n1. /start - запуск взаимодействия со мной.\n' + 
            '2. /status - просмотр статусов всех отчётов, которые ещё не были ' + 
            'сформированы.\n3. /rule - ознакомление с правилами отправки файлов.\n\n' + 
            'Как я работаю?\n\n1. Ты отправляешь мне файл, придерживаясь всех правил.\n' + 
            '2. Я его отправляю на сервер для дальнейшего экспортирования в отчёт и ' + 
            'конвертирование в нужный формат.\n3. Я отправлю тебе отчёт в формате ' +
            '.pdf, как только он будет готов.')

    async def StatusMessage(Message: aiogram.types.Message) -> None: 
        """
        Reaction to command '/status'.

        :param aiogram.types.Message Message: 
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message)
        #   Reaction on /status
        await Activity.ReactionOnStatusText(Info.get('UserID'))
    
    async def RuleMessage(Message: aiogram.types.Message) -> None: 
        """
        Reaction to command '/rule'.

        :param aiogram.types.Message Message: 
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message)
        #   Send message with rule
        await bot.send_message(Info.get('UserID'), 'Правила отправки файлов:\n\n' +
            '1. Названия файлов не должны повторяться, иначе я не смогу помочь ' + 
            'тебе.\n2. Размер файла не должен превышать 20 Мб.\n3. Файлы должны' +
            ' иметь 2 вида расширений, а именно .fpx или .frx')

    async def ReplyMessage(Message: aiogram.types.Message) -> None: 
        """
        Reaction to text sent by user.

        :param aiogram.types.Message Message: 
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message)
        #   If user use ReplyKeyboardButton with text 'Статус'
        if Info.get('Text').lower() == 'статус':
            await Activity.ReactionOnStatusText(Info.get('UserID'))
        #   If user use ReplyKeyboardButton with text 'История'
        if Info.get('Text').lower() == 'история': 
            await Activity.ReactionOnHistoryText(Info.get('UserID'))

    async def GetDocument(Message: aiogram.types.Message) -> None: 
        """
        Reaction on documents thrown off by user.

        1. Preparation basic info
        2. Download document
        3. If previous action is True send message about success.
        4. Add document to queue.
        5. Send message with success about append document to queue
        6. If second action is False send message about fail

        :param aiogram.types.Message Message:
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message) 
        #   Download file depends on user id 
        if await Template.DownloadDocument(Info.get('UserID'), Info.get('FileName'), 
                Info.get('FileID')):
            #   Send message about success download
            await bot.send_message(Info.get('UserID'), f'Файл {Info.get("FileName")}' +
                ' успешно сохранён.')
            #   Add document in queue
            Template.AddDocumentInQueue(
                Info.get('UserID'), Template.GetNumberOfQueue(),
                Info.get('FileName'), Template.MakePath(
                    Info.get('UserID'), 'Template', Info.get('FileName'))
                )
            #   send message about success append to queue
            await bot.send_message(Info.get('UserID'), f'Файл {Info.get("FileName")}' + 
                ' успешно добавлен в очередь.')
        else:
            #   Send message about fail 
            await bot.send_message(Info.get('UserID'), 'Формат или размер файла не ' +
                'соответствует моим правилам!\nЧтобы их узнать введи /rule.\nКогда' +
                ' ознакомишься со всеми правилами, попробуй ещё раз отправить мне ' +
                'файл, может в следующий раз повезёт.')
        
    async def ReactionOnStatusText(UserID: str) -> None: 
        """
        Reaction on ReplyKeyboardButton 'Статус'.

        1. Preparation text.
        2. Send message.

        :param str UserID:
        :return None:
        """
        #   Preparation text
        Text = Template.PrepareBotText(
            Template.GetAllUsersArray(UserID)
            )
        #   Send message about status of all document
        await bot.send_message(UserID, Text)

    async def ReactionOnHistoryText(UserID: str) -> None: 
        """
        Reaction on ReplyKeyboardButton 'История'.

        1. Get list of files inside Template folder.
        2. Create dict.
        3. Preparation text.
        4. Send message.
        5. Active state

        :param str UserID:
        :return None:
        """
        #   Get list of files inside Template folder
        FileList = Template.GetListOfFiles(UserID)
        #   Create dict
        Template.CreateDictOfFiles(UserID, FileList)
        #   Preparation text
        BotText = Template.PrepareTextHistory(UserID)
        #   Send message
        await bot.send_message(UserID, BotText)
        #   Active state
        await RegistrationState.DocIndex.set()

    async def ReactionOnState(Message: aiogram.types.Message, 
        state: aiogram.dispatcher.storage.FSMContext) -> None:
        """
        Reaction on state - DocIndex.

        1. Check type of text.
        2. Check range.
        3. Send file.

        :param aiogram.types.Message Message:
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message) 
        #   Check type of text
        if not Checks.CheckTypeOfIndexDocument(Info.get('Text')):
            await bot.send_message(Info.get('UserID'), 'Номер документы должен' \
                ' состоять из цифр. Например, 1.\nПопробуй ещё раз.')
            return None
        if not Checks.CheckRangeOfDocument(Info.get('UserID'), int(Info.get('Text'))): 
            await bot.send_message(Info.get('UserID'), 'Нет такого номера документа!' \
                '\nПопробуй ещё раз.')
            return None
        #   Set user id and index of document in the same place
        Template.ConnectUserDocument(Info.get('UserID'), int(Info.get('Text')))
        BotMessage = await bot.send_message(Info.get('UserID'), 'Отлично!\nОсталось выбрать' \
            ' формат файла, в котором хочешь видеть отчёт.',
            reply_markup = Template.CreateKeyboardByInsert(
                Template.UniteKeyboardBySubgroup(
                    'FileSystem', Settings.Keyboard.copy()), 'Inline'))
        #   Add message id and user id in the same place
        Template.AddMessageIDToUser(Info.get('UserID'), BotMessage)
        #   Finish state 
        await state.finish()












