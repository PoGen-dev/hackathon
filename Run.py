import aiogram
import threading

from Package.Source.Main import dispatcher
from Package.Source.BotTemplate import Template

if __name__ == '__main__': 
    print('Start polling')
    NewThread = threading.Thread(target = Template.CreatingTarget)
    NewThread.start()    
    aiogram.executor.start_polling(dispatcher)