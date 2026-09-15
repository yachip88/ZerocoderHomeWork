import asyncio
from pathlib import Path

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile, Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"
VOICE_FILE = BASE_DIR / "voice.ogg"


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Пришлите фото — сохраню в папку img.\n"
        "/voice — голосовое сообщение.\n"
        "Любой текст переведу на английский."
    )


@dp.message(Command("voice"))
async def send_voice(message: Message):
    if not VOICE_FILE.exists():
        await message.answer("Файл голосового сообщения не найден.")
        return
    await message.answer_voice(FSInputFile(VOICE_FILE))


@dp.message(F.photo)
async def save_photo(message: Message):
    IMG_DIR.mkdir(exist_ok=True)
    photo = message.photo[-1]
    destination = IMG_DIR / f"{photo.file_id}.jpg"
    await bot.download(photo, destination=destination)
    await message.answer("Фото сохранено в папку img.")


@dp.message(F.text)
async def translate_text(message: Message):
    text = message.text.strip()
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": "ru|en"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                data = await resp.json()
        translated = data["responseData"]["translatedText"]
        await message.answer(translated)
    except Exception:
        await message.answer("Не удалось перевести текст.")


async def main():
    if not TOKEN:
        raise RuntimeError("Укажите TELEGRAM_BOT_TOKEN в файле .env")
    IMG_DIR.mkdir(exist_ok=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
