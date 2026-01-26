
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from config import TELEGRAM_BOT_TOKEN
import db
from onec_client import (
    get_debt,
    get_schedule,
    get_progress,
    get_attendance
)
from utils import (
    format_debt_message,
    format_schedule_message,
    format_progress_message,
    format_attendance_message
)

# ---------------- INIT ----------------

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# ---------------- START ----------------

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Здравствуйте!\n\n"
        "Я телеграм-бот системы информирования студентов.\n\n"
        "Доступные команды:\n"
        "/bind — привязка зачетной книжки\n"
        "/debt — задолженность\n"
        "/schedule — расписание\n"
        "/progress — успеваемость\n"
        "/attendance — посещаемость\n"
        "/help — помощь"
    )

# ---------------- HELP ----------------

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/bind — привязка зачетной книжки\n"
        "/debt — задолженность\n"
        "/schedule — расписание\n"
        "/progress — успеваемость\n"
        "/attendance — посещаемость"
    )

# ---------------- BIND ----------------

@dp.message(Command("bind"))
async def cmd_bind(message: Message):
    await message.answer(
        "Отправьте номер зачетной книжки в формате:\n\n"
        "`зачетка 24ВИТТЕ001`",
        parse_mode="Markdown"
    )


@dp.message(F.text.lower().startswith("зачетка"))
async def bind_process(message: Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            "Неверный формат.\n"
            "Пример:\n"
            "`зачетка 24ВИТТЕ001`",
            parse_mode="Markdown"
        )
        return

    student_code = parts[1].strip()
    telegram_id = message.from_user.id

    db.add_student(telegram_id)
    db.bind_student_code(telegram_id, student_code)

    await message.answer(
        "✅ Привязка выполнена успешно!\n\n"
        f"Зачетная книжка: {student_code}"
    )

# ---------------- DEBT ----------------

@dp.message(Command("debt"))
async def cmd_debt(message: Message):
    telegram_id = message.from_user.id
    student_code = db.get_student_by_telegram(telegram_id)

    if not student_code:
        await message.answer("Сначала выполните привязку через /bind")
        return

    data = get_debt(student_code)
    await message.answer(format_debt_message(data))

# ---------------- SCHEDULE ----------------

@dp.message(Command("schedule"))
async def cmd_schedule(message: Message):
    telegram_id = message.from_user.id
    student_code = db.get_student_by_telegram(telegram_id)

    if not student_code:
        await message.answer("Сначала выполните привязку через /bind")
        return

    data = get_schedule(student_code)
    await message.answer(format_schedule_message(data))

# ---------------- PROGRESS ----------------

@dp.message(Command("progress"))
async def cmd_progress(message: Message):
    telegram_id = message.from_user.id
    student_code = db.get_student_by_telegram(telegram_id)

    if not student_code:
        await message.answer("Сначала выполните привязку через /bind")
        return

    data = get_progress(student_code)
    await message.answer(
        format_progress_message(data),
        parse_mode="Markdown"
    )

# ---------------- ATTENDANCE ----------------

@dp.message(Command("attendance"))
async def cmd_attendance(message: Message):
    telegram_id = message.from_user.id
    student_code = db.get_student_by_telegram(telegram_id)

    if not student_code:
        await message.answer("Сначала выполните привязку через /bind")
        return

    data = get_attendance(student_code)
    await message.answer(
        format_attendance_message(data),
        parse_mode="Markdown"
    )

# ---------------- MAIN ----------------

async def main():
    db.init_db()
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
