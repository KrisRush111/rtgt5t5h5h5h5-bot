import asyncio
import requests
import threading
import http.server
import os
import socketserver
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage

# Токен бота
TOKEN = "7809691512:AAHmFFAGkXu34oW3IujqoTcTmiwzs66Hwe0"

# URL сервера FastAPI
SERVER_URL = "https://server-holiaruss.onrender.com/set_user"  # Исправленный URL

# URL мини-приложения и меню
MENU_URL = "https://krisrush111.github.io/Holiarus-9/menu.html"
MINI_APP_URL = "https://t.me/holiarus_bot/Holiarus"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Фейковый сервер запущен на порту {port}")
        httpd.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

def send_user_data(user_id, user_name):
    try:
        response = requests.post(SERVER_URL, json={"user_id": user_id, "user_name": user_name})
        print("Ответ сервера:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки данных на сервер: {e}")


# Функция для отправки данных пользователя на сервер (async)
async def send_user_data(user_id: int, user_name: str):
    try:
        response = requests.post(SERVER_URL, json={"user_id": user_id, "user_name": user_name})
        response.raise_for_status()
        print("Ответ сервера:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки данных на сервер: {e}")

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Отправляем данные пользователя на сервер
    await send_user_data(user_id, user_name)

    # Создаем кнопки
    builder = InlineKeyboardBuilder()
    builder.button(text="Подписаться на канал", url="https://t.me/holiarus")
    builder.button(text="Играть в 1 клик🐵", url=MINI_APP_URL)  # Открываем мини-приложение Telegram
    builder.adjust(1)

    # Отправляем приветственное сообщение
    await message.answer(
        f'Привет, {user_name}! Добро пожаловать в Holiarus 🐵.\n\n'
        'Теперь ты — участник захватывающего прыжкового приключения! Прыгай по платформам, преодолевай '
        'препятствия и осваивай новые навыки. Игра находится в активной разработке, и мы оценим твои успехи '
        'в будущих обновлениях.\n\n'
        'Зови друзей — вместе вы сможете добиться ещё больших высот!\n\n',
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

# Обработчик команды /help
@dp.message(F.text == '/help')
async def help_cmd(message: types.Message):
    await message.answer('Игра на стадии разработки, возможны сбои и изменения в геймплее. Благодарим за понимание! 🫠')

# Обработчик неизвестных команд
@dp.message(F.text)
async def unknown_command(message: types.Message):
    await message.answer('Вы ввели неизвестную команду')

# Основная функция запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
