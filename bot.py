from aiogram import Bot, Dispatcher
import asyncio

TOKEN = "7781455167:AAGvyYjViBDEEXxPRofSYgJ7nAnmlAINLbg"

bot = Bot(token=TOKEN)
dp = Dispatcher()
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
