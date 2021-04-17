import aiogram
import pathlib
import urllib

from aiogram.contrib.fsm_storage import memory

from .Settings import Settings


bot = aiogram.Bot(token=Settings.TOKEN)
dispatcher = aiogram.Dispatcher(bot, storage = memory.MemoryStorage())

class Template: 

    def CreateKeyboardByInsert(Data: list, Option: str) -> aiogram.types.InlineKeyboardMarkup:
        """
        Creat InlineKeyboardMarkup.

        :param list Data: [[text, callback_data], ...],
        :param str Option: choosen type of keyboard 
        :return [InlineKeyboardMarkup, ReplyKeyboardMarkup]:
        """
        #   Check type of data and parametr
        if isinstance(Data, list) and Option == 'Inline':
            #   Create object InlineKeyboardMarkup
            Keyboard = aiogram.types.InlineKeyboardMarkup(resize_keyboard = True, row_width = 3)
            #   Recursively insert InlineKeyboardButton in InlineKeyboardMarkup
            for Line in Data:
                #   Insert puds inside keyboard
                Keyboard.insert(aiogram.types.InlineKeyboardButton(text = Line[1], callback_data = Line[0]))
            #   Return InlineKeyboardMarkup
            return Keyboard

    def UniteKeyboardBySubgroup(Subgroup: str, AllKeyboard: dict) -> list: 
        """
        Unite keyboard in lists by subgroup.

        :param str Subgroup: subgroup of keyboard
        :param dict AllKeyboard: {0: ('PDF', 'FileSystem'), 1: ('DOCX', 'FileSystem')}
        :return list: [[0, 'PDF'], [1, 'DOCX'], ...]
        """
        #   Make two-dimensional array
        #   Recursively making a lot of smal array depens on Subgroup
        #   key - callback_data (type - int)
        #   value[0] - text (type - str)
        return [[key, value[0]] for key, value in AllKeyboard.items() if value[1] == Subgroup] 

    def PreparationBasicInfo(Message: aiogram.types.Message = None, 
        CallbackQuery: aiogram.types.callback_query.CallbackQuery = None) -> dict: 
        """
        Get special information from Message or CallbackQuery.

        :param aiogram.types.Message Message: 
        :param aiogram.types.callback_query.CallbackQuery CallbackQuery:
        :return dict: {'userID': user id, ...}
        """
        InfoDict = {}
        if Message: 
            InfoDict['UserID'] = str(Message.chat.id)
            InfoDict['Text'] = Message.text
            if Message.document: 
                InfoDict['FileName'] = Message.document.file_name
                InfoDict['FileID'] = Message.document.file_id
        if CallbackQuery: 
            InfoDict['UserID'] = CallbackQuery.from_user.id
            InfoDict['Code'] = int(CallbackQuery.data)
            InfoDict['TextButton'] = Settings.Keyboard.get(InfoDict['Code'])[0]
        return InfoDict

    def CreateDefaultFileSystem(UserID: str) -> None: 
        """
        Create common structure of file system.
        
        - FileSystem -
                      | - UserID - 
                      |            | - PDF
                      |            | - DOCX
                      |            | - SVG
                      |            | - Template
                      | - UserID - 
        
        :param str UserID: User's ID of Telegram 
        :return NoneType: 
        """
        #   Make path to folder by user id inside FileSystem
        PathToSystem = pathlib.Path(str(pathlib.Path(__file__).parents[2]) + '\\FileSystem\\' + UserID)
        #   Create folder by user id in not exists 
        if not PathToSystem.is_dir(): PathToSystem.mkdir()
        #   Recursively create folder inside user's folder
        for Path in Settings.TemplateFileSystem: 
            #   Make path to folder by format of docs + template inside user's folder
            PathToUserFolder = pathlib.Path(str(PathToSystem) + '\\' + Path)
            #   Create folder if not exists
            if not PathToUserFolder.is_dir(): PathToUserFolder.mkdir()

    async def DownloadDocument(UserID: str, FileName: str, FileID: str) -> bool: 
        """
        Download document with format like .frx or .fpx.

        1. Check format of file
        2. Get file info
        3. Download file in FileSystem -> Template

        :param str UserID:
        :param str FileName:
        :param str FileID: 
        :return bool:
        """
        if True:
            try:
                #   get file info
                FileInfo = await bot.get_file(FileID)
                #    Download uploaded file
                urllib.request.urlretrieve('http://api.telegram.org/file/bot' \
                    f'{Settings.TOKEN}/{FileInfo.file_path}',
                    str(pathlib.Path(__file__).parents[2]) + '\\FileSystem\\' + 
                    UserID + f'\\Template\\{FileName}')
                return True
            except:
                pass
        return False
