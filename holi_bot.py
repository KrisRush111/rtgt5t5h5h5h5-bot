import asyncio
import requests
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
SERVER_URL = "https://server-for-holi.onrender.com/save_user"
MENU_URL = "https://krisrush111.github.io/Holiarus-8/menu.html"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Фейковый сервер запущен на порту {port}")
        httpd.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    try:
        requests.post(SERVER_URL, json={"id": user_id, "name": user_name})
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки данных на сервер: {e}")

    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти на канал", url="https://t.me/holiarus")
    builder.button(text="Играть в 1 клик🐵", url="https://t.me/holiarus_bot/Holiarus")

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
    await message.answer('Игра на стадии разработки, возможны сбои и изменения в геймплее. Благодарим за понимание! 🫠')

@dp.message(F.text)
async def unknown_command(message: types.Message):
    await message.answer('Вы ввели неизвестную команду')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')