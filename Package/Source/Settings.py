from .BasicKeyboard import Keyboard

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
    TemplateFileSystem = ['PDF', 'DOCX', 'CVG', 'Template']