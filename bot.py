
import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Логирование
logging.basicConfig(level=logging.INFO)

# Получение токена и конфигураций
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")

# Google Sheets авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я готов помочь с документами.")

@dp.message()
async def search_docs(message: Message):
    query = message.text.lower()
    rows = sheet.get_all_values()
    results = []
    for row in rows:
        if any(query in cell.lower() for cell in row):
            results.append(" | ".join(row))
    if results:
        await message.answer("\n\n".join(results[:5]))
    else:
        await message.answer("Ничего не найдено. Попробуйте другой запрос.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
