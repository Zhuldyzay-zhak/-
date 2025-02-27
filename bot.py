import os
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 1. Убедись, что API-токен загружается корректно
API_TOKEN = os.getenv("API_TOKEN")  # Токен должен быть установлен в переменной окружения!

if not API_TOKEN:
    raise ValueError("API_TOKEN отсутствует! Установите переменную окружения.")

# 2. Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 3. Подключение к базе данных
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT,
    interests TEXT
)
""")
conn.commit()

# 4. Клавиатура
kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Найти подругу"), KeyboardButton(text="Мой профиль")]],
                         resize_keyboard=True)

# 5. Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я помогу тебе найти подругу 😊", reply_markup=kb)

# 6. Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
