import asyncio
import requests
import os
import aiohttp
import threading
import xmltodict
import http.server
import socketserver
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

TOKEN = "7596863518:AAF-XgN9avfFyDOej2-js38DVGL3DY3OdL0"
SERVER_URL = "https://server-for-holi-111.onrender.com/save_user"
MENU_URL = "https://krisrush111.github.io/Holiarus-11/"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# Функция для запуска фейкового HTTP-сервера
def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Фейковый сервер запущен на порту {port}")
        httpd.serve_forever()

# Запускаем сервер в отдельном потоке
threading.Thread(target=keep_alive, daemon=True).start()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name
    user_name = user_name.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")  # Экранирование символов

    # Отправка данных пользователя на сервер
    try:
        response = requests.post(SERVER_URL, json={"id": user_id, "name": user_name})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки данных на сервер: {e}")

    # Создание inline-клавиатуры
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти на канал", url="https://t.me/holiarus")],
        [InlineKeyboardButton(text="Играть в 1 клик🐵", web_app=types.WebAppInfo(url=f"{MENU_URL}?userId={user_id}"))],
        [InlineKeyboardButton(text='Пригласить друзей', switch_inline_query='🚀Присоединяйся к игре и получи бонусы 🚀! https://t.me/holiarus_bot?start=_tgr_hFp2_jY3NjIy')]

    ])

    await message.answer(
        f'Привет, <b>{user_name}</b>! Добро пожаловать в Holiarus 🐵.\n\n'
        'Теперь ты — участник захватывающего прыжкового приключения! Прыгай по платформам, преодолевай '
        'препятствия и осваивай новые навыки. Игра находится в активной разработке, и мы оценим твои успехи '
        'в будущих обновлениях.\n\n'
        'Зови друзей — вместе вы сможете добиться ещё больших высот!\n\n',
        reply_markup=keyboard
    )















async def fetch_xml(session, url):
    async with session.get(url) as response:
        return await response.text()

@dp.message(F.text == '/dollar')
async def dollar(message: types.Message):
    # URL для получения XML-файла с курсами валют от ЦБ РФ
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    async with aiohttp.ClientSession() as session:
        xml_data = await fetch_xml(session, url)
        data_dict = xmltodict.parse(xml_data)

        # Поиск записи с валютой USD
        valutes = data_dict['ValCurs']['Valute']
        for valute in valutes:
            if valute['CharCode'] == 'USD':
                value = float(valute['Value'].replace(',', '.'))
                nominal = int(valute['Nominal'])
                rate = value / nominal
                await message.answer(f"Текущий курс доллара США: {rate:.4f} руб.")
                break
        else:
            await message.answer("Не удалось найти информацию о курсе доллара.")







@dp.message(F.text == '/help')
async def help_cmd(message: Message):
    await message.answer('Игра на стадии разработки, возможны сбои и изменения в геймплее. Благодарим за понимание! 🫠')

@dp.message(F.text)
async def unknown_command(message: Message):
    keyboard=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти на канал", url="https://t.me/holiarus")]])
    await message.answer('Подписывайтесь на наш канал:)',reply_markup=keyboard)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
