from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
import logging
import asyncio
import aiohttp
import os

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_HOST = 'https://sqlchallengestart-bot.onrender.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# --- Кнопки ---
def get_yes_no_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Да", callback_data="answer_yes"),
        InlineKeyboardButton("Нет", callback_data="answer_no")
    )
    return kb

def get_clear_confirm_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Да, очистить", callback_data="confirm_clear"),
        InlineKeyboardButton("Нет", callback_data="cancel_clear")
    )
    return kb

# --- Команда /start ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! 👋")
    await message.answer(
        "Ты хочешь принять участие в SQL Challenge?",
        reply_markup=get_yes_no_keyboard()
    )

# --- Обработка ответа SQL Challenge ---
@dp.callback_query_handler(lambda c: c.data in ["answer_yes", "answer_no"])
async def handle_answer(callback_query: types.CallbackQuery):
    if callback_query.data == "answer_yes":
        await callback_query.message.answer("Тогда плоти денежку! 💸")
    else:
        await callback_query.message.answer("Хорошего дня! ☀️")

# --- Команда /clear с подтверждением ---
@dp.message_handler(commands=['clear'])
async def ask_clear_confirmation(message: types.Message):
    await message.answer(
        "Ты точно хочешь очистить последние сообщения?",
        reply_markup=get_clear_confirm_keyboard()
    )

# --- Обработка подтверждения на очистку ---
@dp.callback_query_handler(lambda c: c.data in ["confirm_clear", "cancel_clear"])
async def handle_clear_response(callback_query: types.CallbackQuery):
    if callback_query.data == "confirm_clear":
        await callback_query.message.answer("Очищаю последние сообщения...")

        try:
            for i in range(20):
                msg_id = callback_query.message.message_id - i
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=msg_id)
        except Exception as e:
            logging.warning(f"Ошибка при удалении: {e}")
    else:
        await callback_query.message.answer("Окей, ничего не трогаю. ❌")

# --- Автопинг ---
async def ping_self():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(WEBHOOK_URL) as resp:
                    print(f"Pinged self: {resp.status}")
        except Exception as e:
            print("Ping error:", e)
        await asyncio.sleep(600)

# --- Webhook ---
async def on_startup(dp):
    asyncio.create_task(ping_self())
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

# --- Запуск ---
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
