from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
import sqlite3

API_TOKEN = "ТВОЙ_ТОКЕН"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Подключение к базе данных
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                age INTEGER, 
                city TEXT, 
                interests TEXT, 
                photo TEXT)""")
conn.commit()

# Кнопки главного меню
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("Найти подругу"), KeyboardButton("Мой профиль"))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        await message.answer("Ты уже зарегистрирована!", reply_markup=kb)
    else:
        await message.answer("Привет! Как тебя зовут?")
        dp.register_message_handler(get_name)

async def get_name(message: types.Message):
    name = message.text
    user_id = message.from_user.id
    dp.register_message_handler(get_age, state={'name': name})

async def get_age(message: types.Message, state):
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введи возраст цифрами!")
        return
    state['age'] = int(age)
    await message.answer("В каком ты городе?")
    dp.register_message_handler(get_city, state=state)

async def get_city(message: types.Message, state):
    city = message.text
    state['city'] = city
    await message.answer("Какие у тебя интересы? (через запятую)")
    dp.register_message_handler(get_interests, state=state)

async def get_interests(message: types.Message, state):
    interests = message.text
    state['interests'] = interests
    await message.answer("Отправь свою фотографию")
    dp.register_message_handler(get_photo, content_types=types.ContentType.PHOTO, state=state)

async def get_photo(message: types.Message, state):
    photo_id = message.photo[-1].file_id
    state['photo'] = photo_id
    user_id = message.from_user.id
    
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
                   (user_id, state['name'], state['age'], state['city'], state['interests'], state['photo']))
    conn.commit()
    
    await message.answer(f"Регистрация завершена, {state['name']}! Теперь можешь искать подруг.", reply_markup=kb)

@dp.message_handler(lambda message: message.text == "Найти подругу")
async def find_friend(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT city, interests, age FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        city, interests, age = user
        cursor.execute("SELECT * FROM users WHERE city=? AND id!=? AND ABS(age - ?) <= 5", (city, user_id, age))
        matches = cursor.fetchall()
        
        if matches:
            friend = matches[0]
            photo = friend[5]
            await bot.send_photo(message.chat.id, photo, caption=f"Нашлась подруга: {friend[1]}, {friend[2]} лет. Интересы: {friend[4]}")
        else:
            await message.answer("К сожалению, пока нет подходящих подруг в твоем городе 😞")
    else:
        await message.answer("Сначала зарегистрируйся с помощью /start!")

executor.start_polling(dp, skip_updates=True)
