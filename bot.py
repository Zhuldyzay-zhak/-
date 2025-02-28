from aiogram import Bot, Dispatcher
import os

TOKEN = os.getenv("API_TOKEN")  # Подтягиваем токен из переменных среды
bot = Bot(token=TOKEN)
dp = Dispatcher()
