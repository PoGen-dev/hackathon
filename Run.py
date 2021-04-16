import aiogram

from Package.Source.Main import dispatcher


if __name__ == '__main__': 
    print('Start polling')
    aiogram.executor.start_polling(dispatcher)