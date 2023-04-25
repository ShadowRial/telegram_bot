import asyncio
import sqlite3

from aiogram.types import callback_query

from configs import token

# фреймворк для Telegram Bot API
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import json
import keyboards as kb
from db import Database
import logging
import sys

sys.setrecursionlimit(100000000)

# присвоение токена, БД, диспетчера
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
db = Database('database.db')
logging.basicConfig(level=logging.INFO)

with open('address.json') as file:
    address = json.load(file)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    db.add_user(message.from_user.id)
    await message.reply('Это - бот мусорщик, задача которого отслеживать заполненные баки.', reply_markup=kb.menu)

# Отправка массива всех баков
@dp.message_handler(lambda message: 'Показать все баки' in message.text)
async def all_buckets(message: types.Message):
    for i, v in enumerate(address):
        print(address)
        await message.answer(f'Номер: {i + 1} Адрес: {v[1]}')


# Отправка массива заполненных баков
@dp.message_handler(lambda message: 'Показать заполненные баки' in message.text)
async def send_exepts(message: types.Message):
    with open('exepts.json') as file:
        buckets = json.load(file)
    # Проверка на наличие заполненные баков
    if buckets == {}:
        await message.answer("Нет заполненных баков")
    else:
        await message.answer('Сейчас закрыты баки по адрессам: ')
        for k, v in enumerate(buckets):
            await message.answer(address.get(v))



# Отправка сообщения о заполненном баке
async def spam_message():
    print('обрабатывается')
    flag = 'false'
    with open("flag.json", "w") as file:
        json.dump(flag, file, indent=4, ensure_ascii=False)
    users = db.get_users()
    for user in users:
        with open('exepts.json') as file:
            exepts = json.load(file)
        await bot.send_message(user[0], f'Контейнер номер <b>{exepts[0][0]}</b> по адресу <b>{exepts[0][1]}</b> заполнен!',
                               disable_notification=True)


@dp.message_handler(lambda message: 'Оповещения' in message.text)
async def spam(message: types.Message):
    await message.answer('Хотите подключить рассылку сообщений о появлении новых заполненных баков?',
                         reply_markup=kb.spam_message)


@dp.callback_query_handler(text='yes')
async def callback_off(callback: types.CallbackQuery):
    await callback.message.answer('О каких баках хотите получать рассылку?', reply_markup=kb.spam_menu)
    await callback.answer()


# Отключение рассылки
@dp.callback_query_handler(text='off')
async def callback_off(callback: types.CallbackQuery):
    db.set_active(0, callback.from_user.id)
    await callback.message.answer(f'Вам больше не будет приходить рассылка!')
    await callback.answer()


@dp.callback_query_handler(text='all')
async def callback_off(callback: types.CallbackQuery):
    db.set_active(1, callback.from_user.id)
    await callback.answer('Вам будет приходить рассылка!', show_alert=True)
    #await callback.answer('Вы уже получаете рассылку!', show_alert=True)


async def send_message():
    print('принято')
    with open('flag.json') as file:
        flags = json.load(file)
    if 'True' in flags:
        await spam_message()
    await asyncio.sleep(30)
    await send_message()


# Запуск бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_message())
    executor.start_polling(dp, skip_updates=True)