import aiogram

from .BotTemplate import bot, Template

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
        await bot.send_message(Info.get('UserID'), 'Добро пожаловать.\n\nЯ помогу ' +
            'тебе составить отчёт, для этого тебе нужно всего лишь отправить мне ' +
            'файл в формате .frx или .fpx.\n\nОднако есть некоторые ' +
            'правила, которые ты должен соблюдать:\n\n1. Название файлов не должны ' +
            'повторяться, иначе я не смогу помочь тебе.\n2. Размер файла не должен ' +
            'превышать 20 Мб')
    
    async def GetDocument(Message: aiogram.types.Message) -> None: 
        """
        Reaction on documents thrown off by user.

        1. Preparation basic info
        2. 

        :param aiogram.types.Message Message:
        :return NoneType:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message) 
        #   Download file depends on user id 
        if await Template.DownloadDocument(Info.get('UserID'), Info.get('FileName'), 
                Info.get('FileID')):
            await bot.send_message(Info.get('UserID'), f'Файл {Info.get("FileName")}' +
                ' успешно сохранён.')
        else: await bot.send_message(Info.get('UserID'), 'Формат или размер файла не ' +
                'соответствует моим требованиям!\n\nПопробуй ещё раз отправить мне ' +
                'файл, может в этот раз повезёт.')
        


















