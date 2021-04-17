from base64 import b64encode

from .BasicKeyboard import Keyboard
from .CryptoKey import DecryptFernet

class Settings:

    #   Bot's token
    TOKEN = '1732186544:AAGF3_ZPKCTO2ktbTgJnzkFqrmYMGoeIdSc'
    #   Queue of files in work
    #   Structure [
    #       
    #       ]
    Queue = []
    #   {0: ('PDF', 'FileSystem'), 1: ('DOCX', 'FileSystem'), ...}
    Keyboard = {Keyboard.index(line): line for line in Keyboard}
    #   Template of File System
    TemplateFileSystem = ['PDF', 'DOCX', 'SVG', 'Template']
    #   Init key for API
    ApiKeyUtf8 = DecryptFernet()
    ApiKeyBase64 = b64encode(f"apikey:{ApiKeyUtf8}".encode()).decode()