import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from .config import TELEGRAM_BOT_TOKEN
from . import db
from .onec_client import get_student_debt, get_student_schedule
from .utils import format_debt_message, format_schedule_message


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Здравствуйте! 👋\n\n"
        "Я бот системы информирования студентов.\n\n"
        "Доступные команды:\n"
        "/bind — привязать аккаунт студента к Telegram\n"
        "/debt — показать задолженности по оплате обучения\n"
        "/schedule — показать расписание занятий\n"
        "/help — помощь\n\n"
        "Сначала выполните привязку с помощью команды /bind."
    )
    await message.answer(text)


@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "Команды:\n"
        "/start — начать работу\n"
        "/bind — привязать аккаунт студента к Telegram\n"
        "/debt — показать задолженности\n"
        "/schedule — показать расписание\n"
        "/help — показать это сообщение"
    )
    await message.answer(text)


@dp.message(Command("bind"))
async def cmd_bind(message: Message):
    text = (
        "Для привязки введите номер зачётной книжки.\n\n"
        "Формат: `зачетка 123456`\n"
        "Например: `зачетка 24ИПОЛ001`"
    )
    await message.answer(text, parse_mode="Markdown")


@dp.message(F.text.lower().startswith("зачетка"))
async def bind_process(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("После слова 'зачетка' укажите номер зачетной книжки.")
        return

    student_id = parts[1].strip()
    telegram_id = message.from_user.id

    # В generic-версии автоматически создаём запись о студенте,
    # в реальной системе лучше сверяться с 1С или внешней БД.
    db.add_student(student_id, full_name=f"Студент {student_id}")
    db.bind_student(telegram_id, student_id)

    await message.answer(
        f"Аккаунт успешно привязан ✅\nНомер зачётной книжки: {student_id}"
    )


@dp.message(Command("debt"))
async def cmd_debt(message: Message):
    telegram_id = message.from_user.id
    student_id = db.get_student_id_by_telegram(telegram_id)
    if not student_id:
        await message.answer("Сначала привяжите аккаунт с помощью команды /bind.")
        return

    data = get_student_debt(student_id)
    if not data or not data.get("success"):
        await message.answer(
            "Не удалось получить информацию о задолженностях.\n"
            "Попробуйте позже или обратитесь к администратору."
        )
        return

    await message.answer(format_debt_message(data))


@dp.message(Command("schedule"))
async def cmd_schedule(message: Message):
    telegram_id = message.from_user.id
    student_id = db.get_student_id_by_telegram(telegram_id)
    if not student_id:
        await message.answer("Сначала привяжите аккаунт с помощью команды /bind.")
        return

    data = get_student_schedule(student_id)
    if not data or not data.get("success"):
        await message.answer(
            "Не удалось получить расписание.\n"
            "Попробуйте позже или обратитесь к администратору."
        )
        return

    await message.answer(format_schedule_message(data))


async def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Configure it in .env.")

    db.init_db()
    print("[BOT] Starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
