import aiogram
import pathlib
import urllib
import os 
import typing
import asyncio
import time 

from aiogram.contrib.fsm_storage import memory

from .Settings import Settings
from .BotChecks import Checks
from .Builder import Builder

bot = aiogram.Bot(token=Settings.TOKEN)
dispatcher = aiogram.Dispatcher(bot, storage = memory.MemoryStorage())

class Template: 

    def CreateKeyboardByInsert(Data: list, Option: str) -> aiogram.types.InlineKeyboardMarkup:
        """
        Creat InlineKeyboardMarkup.

        :param list Data: [[callback_data, text], ...],
        :param str Option: choosen type of keyboard 
        :return [InlineKeyboardMarkup, ReplyKeyboardMarkup]:
        """
        #   Check type of data and parametr
        if isinstance(Data, list) and Option == 'Inline':
            #   Create object InlineKeyboardMarkup
            Keyboard = aiogram.types.InlineKeyboardMarkup(resize_keyboard = True, row_width = 2)
            #   Recursively insert InlineKeyboardButton in InlineKeyboardMarkup
            for Line in Data:
                #   Insert puds inside keyboard
                Keyboard.insert(aiogram.types.InlineKeyboardButton(text = Line[1], callback_data = Line[0]))
            #   Return InlineKeyboardMarkup
            return Keyboard
        #   Check type of data and parametr
        if isinstance(Data, list) and Option == 'Reply':
            #   Create object InlineKeyboardMarkup
            Keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
            #   Recursively insert InlineKeyboardButton in InlineKeyboardMarkup
            for Line in Data:
                #   Insert puds inside keyboard
                Keyboard.insert(aiogram.types.KeyboardButton(Line[1]))
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
            InfoDict['UserID'] = str(CallbackQuery.from_user.id)
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
            '??????????????'
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
        Change status of the first array in queue on '?? ????????????'.

        :return NoneType:
        """
        Settings.Queue[0][4] = '?? ????????????'

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
                Text += f'????????: {Line[2]}:\n??????????????: {Line[1]}\n????????????: {Line[4]}\n\n' \
                        '----------------------------------------\n\n'
            return Text
        return '?????????????? ????????????!'

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
            range(len(ListOfFiles))}
    
    def PrepareTextHistory(UserID: str) -> str: 
        """
        Preparation text about all files which 
        inside Template directory of user.

        :param str UserID: 
        :return str:
        """
        #   Copy global dict 
        DictOfFiles = Settings.History.get(UserID).copy()
        #   If dict isn't empty
        if DictOfFiles:
            Text = '?????????? ?????????? ??????????, ?????????? ???????????????? ???????????? ????????????????.\n\n'
            #   key - number (type int)
            #   value - text (type str) (name of file)
            for key, value in DictOfFiles.items(): 
                Text += f'{str(key)}. {value}\n'
            return Text
        return '???? ?????? ???? ?????????????????? ?????? ??????????.'

    def ConnectUserDocument(UserID: str, Index: int) -> None: 
        """
        Set user id with index of document in the same place. 

        :param str UserID:
        :param int Index:
        """
        Settings.UserWithDocument[UserID] = Index

    def GetNameOfDocument(UserID: str) -> str:
        """
        Get name of document depends on chosen index.

        :param str UserID: 
        :return str:
        """
        #   Copy global dict 
        DictOfFiles = Settings.History.get(UserID).copy()
        #   Return name of file without suffix
        return DictOfFiles.get(Settings.UserWithDocument.get(UserID))

    async def SendDocument(CallbackQuery: aiogram.types.callback_query.CallbackQuery) -> None: 
        """
        Send document with chosen type of document.

        :param aiogram.types.callback_query.CallbackQuery CallbackQuery:
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(CallbackQuery = CallbackQuery) 
        #   Delete InlineKeyboard after the last message
        await bot.edit_message_reply_markup(Info.get('UserID'), 
            Settings.UserMessage.get(Info.get('UserID')), 
            reply_markup = None)
        #   Make path to file
        PathToFile = ''.join([str(pathlib.Path(__file__).parents[2]), 
            '\\FileSystem\\', Info.get('UserID'), f'\\{Info.get("TextButton")}\\',
            Template.GetNameOfDocument(Info.get("UserID")), '.', 
            Info.get("TextButton").lower()])
        #   Send file
        with open(PathToFile, 'rb') as File:
            await bot.send_document(Info.get('UserID'), document = File)

    def AddMessageIDToUser(UserID: str, BotMessage: aiogram.types.Message) -> None: 
        """
        Add message id and user id in the same place.

        :param str UserID: 
        :param aiogram.types.Message BotMessage:
        :return NoneType:
        """
        Settings.UserMessage[UserID] = BotMessage.message_id

    def DeleteLineInQueue() -> None: 
        """
        """
        Settings.Queue.remove(Settings.Queue[0])

    def CreatingTarget():
        """
        """
        #   Make object AbstractEventLoop
        NewLoop = asyncio.new_event_loop()
        #   Run async
        NewLoop.run_until_complete(Template.CheckingQueue())

    def LowweringOfQueue(): 
        """
        """
        Queue = Settings.Queue.copy()
        for Line in Queue: 
            Line[1] = Line[1] - 1 
        Settings.Queue = Queue

    async def CheckingQueue():
        """
        """
        telebot = aiogram.Bot(token=Settings.TOKEN)
        while True:
            Queue = Settings.Queue.copy()
            #   If Queue isn't empty
            if Queue: 
                #   If status of document is '??????????????'
                if Queue[0][4] == '??????????????': 
                    #   Change status to '?? ????????????'
                    Template.ChangeStatus()
                    #   Get content in file
                    with open(Queue[0][3], 'r') as File: Content = File.read()
                    await Template.UploadFile(Queue, Content, telebot)
                    time.sleep(1)
                    FilePath = ''.join([str(pathlib.Path(__file__).parents[2]), '\\FileSystem\\',
                        Queue[0][0], f'\\PDF\\{Queue[0][2][:-4]}.pdf'])
                    await Template.DownloadFile(Queue, FilePath, telebot)
                    time.sleep(1)
                    #   Delete line in queue
                    Template.DeleteLineInQueue()
                    time.sleep(1)
                    #   Lowwering of queue
                    Template.LowweringOfQueue()
                    #   Read document
                    with open(FilePath, 'rb') as File:
                        #   Send document to user
                        await telebot.send_document(Queue[0][0], document = File)
            time.sleep(2) 

    async def UploadFile(Queue, Content, telebot): 
        """
        """
        try: 
            #   Upload file in service
            Builder.Upload(Queue[0][2], Queue[0][0], Content)
        except: 
            await telebot.send_message(Queue[0][0],
            '???????????????? ???????????? ?????? ???????????????? ?????????? ???? ????????????!')

    async def DownloadFile(Queue, FilePath, telebot): 
        """
        """
        try:
            #   Download file
            Builder.Download(Builder.ExportReport(Queue[0][2], ), FilePath)
            ListOfFormat = ['xlsx', 'Docx', 'SVG']
            for Format in ListOfFormat:
                #   Download file
                Builder.Download(Builder.ExportReport(Queue[0][2], Format), 
                    FilePath.replace('PDF', Format.upper()).replace('pdf', Format.lower()))
        except: 
            await telebot.send_message(Queue[0][0],
            '???????????????? ???????????? ?????? ???????????????????? ?????????? ???? ??????????????!')

