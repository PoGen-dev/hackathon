from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Здарова, я бот')

@dp.message_handler(commands=[''])
async def privet(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Здарова')



if __name__ == '__main__':
    executor.start_polling(dp)
