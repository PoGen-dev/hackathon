import aiogram

from .BotTemplate import bot, Template

class Activity: 

    async def StartMessage(Message: aiogram.types.Message) -> None: 
        """
        Reaction on '/start'. 

        1. Preparation basic info
        2. Create default structure in FileSystem
        3. 

        :param aiogram.types.Message Message:
        """
        #   Preparat basic info
        Info = Template.PreparationBasicInfo(Message) 
        #   Create default structure in FileSystem
        Template.CreateDefaultFileSystem(str(Message.chat.id))

        await bot.send_message(Message.chat.id, 'Hello')