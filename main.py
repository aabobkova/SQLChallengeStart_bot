from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
import logging

API_TOKEN = '8174795025:AAFCtxXU2zKS-DJoQVls0RUpgHorhNjKSGo'
WEBHOOK_HOST = 'https://sqlchallengestart-bot.onrender.com'  # ← позже заменим
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Привет!", callback_data='ok'))
    await message.answer("Бот работает!", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'ok')
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Ты нажал кнопку!")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

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
