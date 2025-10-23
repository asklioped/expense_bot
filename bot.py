import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, tz_name
from manager import ExpenseManager
from categories import CATEGORIES


# Додаємо логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера та бізнес-логіки
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
manager = ExpenseManager()

# Словник для тимчасового збереження сум
pending_amounts = {}


# ------------------/start----------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! 👋 Це бот для обліку витрат.\n"
        "Використай /add, щоб додати витрату."
    )


# --------------------/today----------------------------
@dp.message(Command("today"))
async def stats_today(message: types.Message):
    user_id = message.from_user.id
    total = manager.get_today_total(user_id)
    await message.answer(f"📅 Витрати за сьогодні: {total:.2f} грн")


#--------------------/week-------------------------------
@dp.message(Command("week"))
async def stats_week(message: types.Message):
    user_id = message.from_user.id
    total = manager.get_week_delta(user_id)
    await message.answer(f"🗓️ Витрати за поточний тиждень: {total:.2f} грн")


#-------------------/month--------------------------------------
@dp.message(Command("month"))
async def stats_month(message: types.Message):
    user_id = message.from_user.id
    total = manager.get_month_total(user_id)
    await message.answer(f"🗓️ Витрати за поточний місяць: {total:.2f} грн")


#--------------------/time--------------------------------------
@dp.message(Command("time"))
async def show_local_time(message: types.Message):
    await message.answer(f"🕑 Локальний час {manager.local_timestamp_txt(manager.local_timestamp(tz_name))}")        


#--------------------/add-----------------------------------
@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    pending_amounts[message.from_user.id] = None
    await message.answer("Введи суму витрати (Наприклад 250):")


#--------------------обробка введеної суми-------------
@dp.message()
async def process_amount(message: types.Message):
    user_id = message.from_user.id
    if user_id not in pending_amounts:
        return
    if pending_amounts[user_id] is None:
        try:
            amount = float(message.text.replace(",", "."))
            if amount <= 0:
                await message.answer("🙅‍♀️Сума не може бути нульвою\nабо менше нуля\nСпробуй ще раз")
                return
        except ValueError:
            await message.answer("🤦‍♀️Сума має бути числом, спробуй ще раз")
            return
        pending_amounts[user_id] = amount

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=name, callback_data=code)]
                for code, name in CATEGORIES.items()
            ]
        )
        await message.answer(f"Сума {amount:.2f} грн прийнята ✅\nТепер обери категорію:", reply_markup=kb)


# -------------------Обробка вибору категорії----------------
@dp.callback_query()
async def process_category(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in pending_amounts or pending_amounts[user_id] is None:
        await callback.answer("Спочатку введи суму через /add")
        return
    
    amount = pending_amounts.pop(user_id)
    category_code = callback.data
    manager.add_expense(user_id=user_id, amount=amount, category=category_code)

    await callback.message.edit_text(
        f"✅ Витрату {amount:.2f} грн у категорії *{CATEGORIES[category_code]}* додано!",
        parse_mode="Markdown"
    )
    await callback.answer()


# Точка входу
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())