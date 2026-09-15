import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")],
    ],
    resize_keyboard=True,
)

links_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://news.google.com")],
        [InlineKeyboardButton(text="Музыка", url="https://music.youtube.com")],
        [InlineKeyboardButton(text="Видео", url="https://www.youtube.com")],
    ]
)

more_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")],
    ]
)

options_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Опция 1", callback_data="option_1"),
            InlineKeyboardButton(text="Опция 2", callback_data="option_2"),
        ]
    ]
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберите кнопку:", reply_markup=start_keyboard)


@dp.message(F.text == "Привет")
async def hello(message: Message):
    name = message.from_user.first_name or "пользователь"
    await message.answer(f"Привет, {name}!")


@dp.message(F.text == "Пока")
async def bye(message: Message):
    name = message.from_user.first_name or "пользователь"
    await message.answer(f"До свидания, {name}!")


@dp.message(Command("links"))
async def links(message: Message):
    await message.answer("Полезные ссылки:", reply_markup=links_keyboard)


@dp.message(Command("dynamic"))
async def dynamic(message: Message):
    await message.answer("Динамическая клавиатура:", reply_markup=more_keyboard)


@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=options_keyboard)
    await callback.answer()


@dp.callback_query(F.data == "option_1")
async def option_1(callback: CallbackQuery):
    await callback.message.answer("Опция 1")
    await callback.answer()


@dp.callback_query(F.data == "option_2")
async def option_2(callback: CallbackQuery):
    await callback.message.answer("Опция 2")
    await callback.answer()


async def main():
    if not TOKEN:
        raise RuntimeError("Укажите TELEGRAM_BOT_TOKEN в файле .env")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
