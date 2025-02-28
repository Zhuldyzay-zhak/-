from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI
import asyncio
import logging
import os

TOKEN = "7781455167:AAGvyYjViBDEEXxPRofSYgJ7nAnmlAINLbg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настраиваем FastAPI
app = FastAPI()

@app.post("/")
async def webhook(update: dict):
    telegram_update = Update(**update)
    await dp.process_update(telegram_update)

async def main():
    logging.basicConfig(level=logging.INFO)
   await bot.delete_webhook()
await bot.start_polling()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
