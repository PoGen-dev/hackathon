from base64 import b64encode
from aiogram.dispatcher.filters.state import StatesGroup, State
from .BasicKeyboard import Keyboard
from .CryptoKey import DecryptFernet

class Settings:

    #   Bot's token
    TOKEN = '1573602297:AAERBgSxHA1MYod7MJQdmPc-h2U1ZDifwys'
    #   Queue of files in work
    #   Structure [
    #       [UserID, NumberOfQueue, FileName, FilePath],
    #       ...,
    #       ]
    Queue = []
    #   {0: ('PDF', 'FileSystem'), 1: ('DOCX', 'FileSystem'), ...}
    Keyboard = {Keyboard.index(line): line for line in Keyboard}
    #   Template of File System
    TemplateFileSystem = ['PDF', 'DOCX', 'SVG', 'Template', 'XLSX']
    #   Init key for API
    ApiKeyUtf8 = DecryptFernet()
    ApiKeyBase64 = b64encode(f"apikey:{ApiKeyUtf8}".encode()).decode()
    #   Files history
    #   Structure {
    #       UserID: {
    #           Count: FileName
    #           }   
    #       }
    History = {}
    #   Structure {
    #   UserID: IndexOfDocument
    #   }
    UserWithDocument = {}
    #   Structure {
    #   UserID: MessageID
    #   }
    UserMessage = {}

class RegistrationState(StatesGroup): 

    DocIndex = State()