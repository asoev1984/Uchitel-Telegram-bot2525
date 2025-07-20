import logging
import gspread
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils import executor
from oauth2client.service_account import ServiceAccountCredentials

import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")  # Установи переменную окружения BOT_TOKEN в Render

# Google Sheets авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Пример: открыть таблицу
try:
    sheet = client.open("TestSheet").sheet1
except Exception as e:
    sheet = None
    print("Не удалось открыть таблицу:", e)

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Стартовая команда
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает.")

# Пример команды для чтения из таблицы
@dp.message()
async def echo(message: Message):
    if sheet:
        try:
            cell_value = sheet.cell(1, 1).value
            await message.answer(f"Значение в ячейке A1: {cell_value}")
        except Exception as e:
            await message.answer(f"Ошибка чтения таблицы: {e}")
    else:
        await message.answer("Таблица не подключена.")

# Запуск
async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
