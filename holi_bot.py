import asyncio
import aiohttp
import ssl
import certifi
import os
import threading
import http.server
import socketserver
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "7809691512:AAHmFFAGkXu34oW3IujqoTcTmiwzs66Hwe0"
SERVER_URL = "https://server-for-holi-ey6j.onrender.com/set_user"
MENU_URL = "https://krisrush111.github.io/Holiarus-10/menu.html"
MINI_APP_URL = "https://t.me/holiarus_bot/Holiarus"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def keep_alive():
    """Фейковый сервер для поддержки активности на бесплатных хостингах."""
    try:
        port = int(os.environ.get("PORT", 8080))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Фейковый сервер запущен на порту {port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Ошибка запуска keep_alive: {e}")

# Запуск фейкового сервера в отдельном потоке
threading.Thread(target=keep_alive, daemon=True).start()

async def send_user_data(user_id, user_name):
    """Асинхронная отправка user_id и user_name на сервер с поддержкой SSL."""
    ssl_context = ssl.create_default_context(cafile=certifi.where())  # Используем актуальные сертификаты
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(SERVER_URL, json={"user_id": str(user_id), "user_name": user_name}, ssl=ssl_context) as response:
                resp_json = await response.json()
                print("✅ Данные успешно отправлены на сервер:", resp_json)
        except aiohttp.ClientConnectorCertificateError:
            print("⚠️ Проблема с SSL-сертификатом! Пробуем без верификации...")
            async with session.post(SERVER_URL, json={"user_id": str(user_id), "user_name": user_name}, ssl=False) as response:
                resp_json = await response.json()
                print("✅ Данные отправлены (без проверки SSL):", resp_json)
        except Exception as e:
            print(f"❌ Ошибка отправки данных на сервер: {e}")

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработчик команды /start — отправляет user_id на сервер и предлагает запустить игру."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    await send_user_data(user_id, user_name)  # Отправляем данные на сервер

    builder = InlineKeyboardBuilder()
    builder.button(text="Подписаться на канал", url="https://t.me/holiarus")
    builder.button(text="Играть в 1 клик 🐵", url=MINI_APP_URL)  # Открываем мини-приложение Telegram
    builder.adjust(1)

    await message.answer(
        f'Привет, {user_name}! Добро пожаловать в Holiarus 🐵.\n\n'
        'Теперь ты — участник захватывающего прыжкового приключения! Прыгай по платформам, преодолевай '
        'препятствия и осваивай новые навыки. Игра находится в активной разработке, и мы оценим твои успехи '
        'в будущих обновлениях.\n\n'
        'Зови друзей — вместе вы сможете добиться ещё больших высот!\n\n',
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.message(F.text == '/help')
async def help_cmd(message: types.Message):
    """Ответ на команду /help."""
    await message.answer('Игра на стадии разработки, возможны сбои и изменения в геймплее. Благодарим за понимание! 🫠')

@dp.message(F.text)
async def unknown_command(message: types.Message):
    """Обработчик неизвестных команд."""
    await message.answer('Вы ввели неизвестную команду')

async def main():
    """Запуск бота."""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('❌ Бот выключен')
