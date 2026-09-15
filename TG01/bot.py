import asyncio

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

MOSCOW_LAT = 55.75
MOSCOW_LON = 37.62


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я учебный бот.\n"
        "Команды: /start, /help, /weather — погода в Москве."
    )


@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "/start — приветствие\n"
        "/help — справка\n"
        "/weather — текущая температура в Москве"
    )


@dp.message(Command("weather"))
async def weather(message: Message):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={MOSCOW_LAT}&longitude={MOSCOW_LON}&current_weather=true"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                data = await resp.json()
        current = data["current_weather"]
        temp = current["temperature"]
        await message.answer(f"Москва: сейчас {temp}°C.")
    except Exception:
        await message.answer("Не удалось получить прогноз погоды.")


async def main():
    if not TOKEN:
        raise RuntimeError("Укажите TELEGRAM_BOT_TOKEN в файле .env")
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="help", description="Справка"),
            BotCommand(command="weather", description="Погода в Москве"),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
