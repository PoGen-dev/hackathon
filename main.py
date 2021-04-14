from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start',])
async def start(msg: types.Message):
    await msg.reply('пересланное')
    await bot.send_message(msg.from_user.id, 'не пересланное')

if __name__ == '__main__':
    executor.start_polling(dp)
