import asyncio
import sqlite3
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

DB_PATH = Path(__file__).resolve().parent / "school_data.db"


class StudentForm(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT
        )
        """
    )
    conn.commit()
    conn.close()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(StudentForm.name)
    await message.answer("Как тебя зовут?")


@dp.message(StudentForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(StudentForm.age)
    await message.answer("Сколько тебе лет?")


@dp.message(StudentForm.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуй ещё раз.")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(StudentForm.grade)
    await message.answer("В каком ты классе?")


@dp.message(StudentForm.grade)
async def get_grade(message: Message, state: FSMContext):
    data = await state.get_data()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
        (data["name"], data["age"], message.text),
    )
    conn.commit()
    conn.close()
    await state.clear()
    await message.answer("Данные сохранены в school_data.db.")


async def main():
    if not TOKEN:
        raise RuntimeError("Укажите TELEGRAM_BOT_TOKEN в файле .env")
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
