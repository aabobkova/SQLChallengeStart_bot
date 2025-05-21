from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
import logging
import os

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_HOST = 'https://sqlchallengestart-bot.onrender.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# --- Клавиатура с "Да" / "Нет" ---
def get_yes_no_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Да", callback_data="answer_yes"),
        InlineKeyboardButton("Нет", callback_data="answer_no")
    )
    return kb

# --- Старт / Приветствие ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! 👋")
    await message.answer(
        "Ты хочешь принять участие в SQL Challenge?",
        reply_markup=get_yes_no_keyboard()
    )

# --- Обработка ответов на вопрос ---
@dp.callback_query_handler(lambda c: c.data in ["answer_yes", "answer_no"])
async def handle_answer(callback_query: types.CallbackQuery):
    if callback_query.data == "answer_yes":
        await callback_query.message.answer("Тогда плоти денежку! 💸")
    else:
        await callback_query.message.answer("Хорошего дня! ☀️")

# --- Webhook события ---
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

# --- Запуск вебхука ---
if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=10000
    )
