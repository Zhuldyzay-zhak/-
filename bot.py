from aiogram import Bot, Dispatcher, types
import asyncio

TOKEN = "ТВОЙ_ТОКЕН"

bot = Bot(token=TOKEN)
dp = Dispatcher()  # Убери аргумент bot

# Создаём Router и добавляем его
from aiogram import Router

router = Router()
dp.include_router(router)

@router.message()
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)  
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
