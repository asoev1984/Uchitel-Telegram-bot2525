
import os
import logging
import asyncio

import gspread
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from oauth2client.service_account import ServiceAccountCredentials
from aiohttp import web
import uvicorn

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Токен Telegram бота из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

try:
    sheet = client.open("TestSheet").sheet1
except Exception as e:
    sheet = None
    print("Не удалось открыть таблицу:", e)

# Команды
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает.")

@dp.message()
async def echo(message: Message):
    if sheet:
        try:
            value = sheet.cell(1, 1).value
            await message.answer(f"Значение в A1: {value}")
        except Exception as e:
            await message.answer(f"Ошибка чтения таблицы: {e}")
    else:
        await message.answer("Таблица не подключена.")

# FastAPI для Render
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Бот работает"}

# Основной запуск
async def main():
    await dp.start_polling(bot)

if name == "main":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
