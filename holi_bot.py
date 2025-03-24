import asyncio
import requests
import os
import aiohttp
import ssl
import threading
import xmltodict
import http.server
import socketserver
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

TOKEN = "7809691512:AAHmFFAGkXu34oW3IujqoTcTmiwzs66Hwe0"
SERVER_URL = "https://server-for-holi-111-k6qj.onrender.com/save_user"
MENU_URL = "https://krisrush111.github.io/Holiarus-11/menu"

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
        [InlineKeyboardButton(text='📩Пригласить друзей📩',callback_data="invite_friends")]
    ])

    await message.answer(
        f'Привет, <b>{user_name}</b>! Добро пожаловать в Holiarus 🐵.\n\n'
        'Теперь ты — участник захватывающего прыжкового приключения! Прыгай по платформам, преодолевай '
        'препятствия и осваивай новые навыки. Игра находится в активной разработке, и мы оценим твои успехи '
        'в будущих обновлениях.\n\n'
        'Зови друзей — вместе вы сможете добиться ещё больших высот!\n\n',
        reply_markup=keyboard
    )


@dp.callback_query(F.data == 'invite_friends')
async def invite_friends(callback_query: CallbackQuery):
    referral_link = f"https://t.me/holiarus_bot?start={callback_query.from_user.id}"
    await bot.send_message(callback_query.from_user.id, "Ваша реферальная ссылка для приглашения:")
    share_text = (
        "🚀 Присоединяйся, собирай кристаллы и проходи испытания вместе со мной 🚀!\n\n"
        f"{referral_link}\n\n"
    )
    await bot.send_message(callback_query.from_user.id, share_text)
    await callback_query.answer("Ссылка отправлена в личные сообщения!")
























DEBUG_MODE = False  # ← добавь эту строку ВМЕСТО строки с os.getenv


async def fetch_xml(session, url):
    ssl_context = None

    if DEBUG_MODE:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE  # Отключаем проверку сертификатов в dev

    async with session.get(url, ssl=ssl_context) as response:
        return await response.text()


@dp.message(F.text == '/usd')
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
                await message.answer(f"Текущий курс | Доллар США: {rate:.2f} руб.")
                break
        else:
            await message.answer("Не удалось найти информацию о курсе доллара.")





@dp.message(F.text == '/eur')
async def euro(message: types.Message):
    # URL для получения XML-файла с курсами валют от ЦБ РФ
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    async with aiohttp.ClientSession() as session:
        xml_data = await fetch_xml(session, url)
        data_dict = xmltodict.parse(xml_data)

        # Поиск записи с валютой USD
        valutes = data_dict['ValCurs']['Valute']
        for valute in valutes:
            if valute['CharCode'] == 'EUR':
                value = float(valute['Value'].replace(',', '.'))
                nominal = int(valute['Nominal'])
                rate = value / nominal
                await message.answer(f"Текущий курс | Евро: {rate:.2f} руб.")
                break
        else:
            await message.answer("Не удалось найти информацию о курсе доллара.")


@dp.message(F.text == '/aed')
async def dirham(message: types.Message):
    # URL для получения XML-файла с курсами валют от ЦБ РФ
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    async with aiohttp.ClientSession() as session:
        xml_data = await fetch_xml(session, url)
        data_dict = xmltodict.parse(xml_data)

        # Поиск записи с валютой USD
        valutes = data_dict['ValCurs']['Valute']
        for valute in valutes:
            if valute['CharCode'] == 'AED':
                value = float(valute['Value'].replace(',', '.'))
                nominal = int(valute['Nominal'])
                rate = value / nominal
                await message.answer(f"Текущий курс | Дирхам ОАЭ: {rate:.2f} руб.")
                break
        else:
            await message.answer("Не удалось найти информацию о курсе доллара.")



@dp.message(F.text == '/byn')
async def bulba(message: types.Message):
    # URL для получения XML-файла с курсами валют от ЦБ РФ
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    async with aiohttp.ClientSession() as session:
        xml_data = await fetch_xml(session, url)
        data_dict = xmltodict.parse(xml_data)

        # Поиск записи с валютой USD
        valutes = data_dict['ValCurs']['Valute']
        for valute in valutes:
            if valute['CharCode'] == 'BYN':
                value = float(valute['Value'].replace(',', '.'))
                nominal = int(valute['Nominal'])
                rate = value / nominal
                await message.answer(f"Текущий курс | Белорусский рубль: {rate:.2f} руб.")
                break
        else:
            await message.answer("Не удалось найти информацию о курсе доллара.")



@dp.message(F.text == '/uah')
async def cegrivna(message: types.Message):
    # URL для получения XML-файла с курсами валют от ЦБ РФ
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    async with aiohttp.ClientSession() as session:
        xml_data = await fetch_xml(session, url)
        data_dict = xmltodict.parse(xml_data)

        # Поиск записи с валютой USD
        valutes = data_dict['ValCurs']['Valute']
        for valute in valutes:
            if valute['CharCode'] == 'UAH':
                value = float(valute['Value'].replace(',', '.'))
                nominal = int(valute['Nominal'])
                rate = value / nominal
                await message.answer(f"Текущий курс | Гривен: {rate:.2f} руб.")
                break
        else:
            await message.answer("Не удалось найти информацию о курсе доллара.")


@dp.message(F.text == '/mywallet')
async def wallet(message: types.Message):
    pass









@dp.message(F.text == '/help')
async def help_cmd(message: Message):
    await message.answer('Игра на стадии разработки, возможны сбои и изменения в геймплее. Благодарим за понимание! 🫠')

@dp.message(F.text)
async def unknown_command(message: Message):
    keyboard=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти на канал", url="https://t.me/holiarus")]])
    await message.answer('Подписывайтесь на наш канал ',reply_markup=keyboard)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')