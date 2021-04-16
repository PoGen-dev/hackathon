import aiogram

from Source.BotTemplate import dispatcher

if __name__ == '__main__': 
    print('Start polling')
    aiogram.executor.start_polling(dispatcher)