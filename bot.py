import os
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile

# Загружаем API-токен из переменных среды (Render)
API_TOKEN = os.getenv("API_TOKEN")

# Проверяем, что токен загружен корректно
if not API_TOKEN:
    raise ValueError("❌ Ошибка: API_TOKEN не найден! Убедись, что он добавлен в Render.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Подключение к базе данных
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        city TEXT,
        interests TEXT,
        photo TEXT
    )
""")
conn.commit()

# Кнопки главного меню
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("Найти подругу"), KeyboardButton("Мой профиль"))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user:
        await message.answer("Привет! Я тебя помню 😊", reply_markup=kb)
    else:
        cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
        conn.commit()
        await message.answer("Привет! Добро пожаловать в бота для поиска подруг! 🩷", reply_markup=kb)

# Запуск бота
async def main():
    print("🤖 Бот запущен и ждёт команды!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
