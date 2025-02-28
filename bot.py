import asyncio
from aiogram import Bot, Dispatcher

TOKEN = "7781455167:AAGvyYjViBDEEXxPRofSYgJ7nAnmlAINLbg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await bot.delete_webhook()  # Удаляем Webhook
    await dp.start_polling()  # Запускаем бота

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
