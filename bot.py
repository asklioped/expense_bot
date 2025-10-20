import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

# Додаємо логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start
@dp.message()
async def start(message):
    await message.answer("Привіт! Це бот для обліку витрат. Використай /add для початку.")

# Точка входу
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
