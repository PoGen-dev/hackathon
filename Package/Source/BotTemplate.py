import aiogram
import pathlib
import urllib
import os 
import typing

from aiogram.contrib.fsm_storage import memory

from .Settings import Settings
from .BotChecks import Checks

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
        #   Recursively making a lot of small array depens on Subgroup
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
        if Checks.CheckTypeDocument(FileName):
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

    def AddDocumentInQueue(UserID: str, NumberOfQueue: int, FileName: str, FilePath: str) -> None: 
        """
        Add document in queue.

        :param str UserID:
        :param int NumberOfQueue: 
        :param str FileName: 
        :param str FilePath:
        :return NoneType:
        """
        Settings.Queue.append([
            UserID,
            NumberOfQueue,
            FileName,
            FilePath,
            'Очередь'
            ])

    def GetNumberOfQueue() -> int: 
        """
        Get the last number of queue.

        :return int:
        """
        #   Try to getting first array in queue
        try: Settings.Queue[0]
        #   If queue is empty return default number of queue
        except IndexError: return 1
        #   If queue is not empty, return the last number
        #   of queue + 1 
        return Settings.Queue[-1][1] + 1

    def MakePath(UserID: str, FolderName: str, FileName: str) -> str: 
        """
        Make path to file inside FileSystem depends on user id 
        and folder name.

        :param str UserID: 
        :param str FolderName: 
        :param str FileName:
        :return str PathToFile:
        """
        PathToFile = ''.join([str(pathlib.Path(__file__).parents[2]), '\\FileSystem\\',
            UserID, '\\', FolderName, '\\', FileName]) 
        return PathToFile

    def ReadFile(PathToFile: str) -> bytes: 
        """
        Read file in rb mode.

        :param str PathToFile: 
        :return bytes: 
        """
        #   Open file in rb mode
        with open(PathToFile, 'rb') as File: 
            #   Get and return content 
            return File.read()

    def ChangeStatus() -> None: 
        """
        Change status of the first array in queue on 'В работе'.

        :return NoneType:
        """
        Settings.Queue[0][4] = 'В работе'

    def GetAllUsersArray(UserID: str) -> typing.Union[list, bool]: 
        """
        Get all array with status depends on user.

        :param str UserID: 
        :return list:
        """
        #   Copy main queue
        AllArray = Settings.Queue.copy()
        #   If AllArray isn't empty, search array with user id 
        if AllArray: return [Array for Array in AllArray if Array[0] == UserID]
        return False

    def PrepareBotText(Array: list) -> str: 
        """
        Depends on array choose text for bot sending.

        :param list Array:
        :return str:
        """
        if Array: 
            Text = ''
            for Line in Array:
                Text += f'Файл: {Line[2]}:\nОчередь: {Line[1]}\nСтатус: {Line[4]}\n\n' \
                        '----------\n\n'
            return Text
        return 'Очередь пустая!'

    def GetListOfFiles(UserID: str) -> list: 
        """
        Get list with all file's names in FileSystem\\Template.

        :param str UserID: 
        :return list:
        """
        PathToDirectory = str(pathlib.Path(__file__).parents[2]) + '\\' \
            'FileSystem\\' + UserID + '\\Template\\'
        FileList = [File.replace('.fpx', '').replace('.frx', '') for File 
            in os.listdir(PathToDirectory)]
        return FileList

    def CreateDictOfFiles(UserID: str, ListOfFiles: list) -> None: 
        """
        Create dict of files. In futures for creating text of message
        to user. 

        :param str UserID:
        :param list ListOfFiles:
        :return NoneType:
        """
        Settings.History[UserID] = {Index + 1: ListOfFiles[Index] for Index in 
            len(ListOfFiles)}
    
    def PrepareTextHistory(UserID: str) -> str: 
        """
        Preparation text about all files which 
        inside Template directory of user.

        :param str UserID: 
        :return str:
        """
        #   Copy global dict 
        DictOfFiles = Settings.History[UserID].copy()
        #   If dict isn't empty
        if DictOfFiles:
            Text = 'Введи номер файла, отчёт которого хочешь получить.\n\n'
            #   key - number (type int)
            #   value - text (type str) (name of file)
            for key, value in DictOfFiles.items(): 
                Text += f'{str(key)}. {value}\n'
            return Text
        return 'Ты ещё не отправлял мне файлы.'
