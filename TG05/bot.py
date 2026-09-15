import asyncio
import random

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Бот с внешними API.\n"
        "/cat — случайная порода кошки (TheCatAPI)\n"
        "/joke — случайная шутка"
    )


@dp.message(Command("cat"))
async def random_cat(message: Message):
    url = "https://api.thecatapi.com/v1/breeds"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                breeds = await resp.json()
        breed = random.choice(breeds)
        name = breed.get("name", "кот")
        desc = breed.get("temperament", "")
        image_url = "https://api.thecatapi.com/v1/images/search"
        params = {"breed_ids": breed.get("id")}
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                photos = await resp.json()
        photo = photos[0]["url"] if photos else None
        text = f"{name}\n{desc}"
        if photo:
            await message.answer_photo(photo, caption=text)
        else:
            await message.answer(text)
    except Exception:
        await message.answer("Не удалось получить данные о кошках.")


@dp.message(Command("joke"))
async def random_joke(message: Message):
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                data = await resp.json()
        await message.answer(f"{data['setup']}\n{data['punchline']}")
    except Exception:
        await message.answer("Не удалось получить шутку.")


async def main():
    if not TOKEN:
        raise RuntimeError("Укажите TELEGRAM_BOT_TOKEN в файле .env")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
