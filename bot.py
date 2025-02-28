import asyncio
from aiogram import Bot, Dispatcher

TOKEN = "7781455167:AAGvyYjViBDEEXxPRofSYgJ7nAnmlAINLbg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await bot.delete_webhook()  # убедитесь, что этот код имеет правильный отступ
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
