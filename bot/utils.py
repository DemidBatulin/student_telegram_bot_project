def format_debt_message(data: dict) -> str:
    """
    Форматирование ответа по задолженности
    """
    payload = data.get("data") or {}

    debts = payload.get("debts")
    if not debts:
        return "Задолженности не обнаружено ✅"

    lines = ["📌 *Задолженность по обучению:*"]
    for item in debts:
        name = item.get("name", "—")
        amount = item.get("amount", "—")
        lines.append(f"• {name}: {amount} ₽")

    return "\n".join(lines)


def format_schedule_message(data: dict) -> str:
    """
    Форматирование расписания
    """
    payload = data.get("data") or {}
    schedule = payload.get("schedule")

    if not schedule:
        return "Расписание временно недоступно ❌"

    lines = ["📅 *Расписание занятий:*"]
    for row in schedule:
        time = row.get("time", "")
        subject = row.get("discipline", "")
        room = row.get("auditory", "")
        lines.append(f"{time} — {subject} ({room})")

    return "\n".join(lines)


def format_progress_message(data: dict) -> str:
    """
    Форматирование успеваемости
    """
    payload = data.get("data") or {}
    grades = payload.get("grades")

    if not grades:
        return "Данные об успеваемости отсутствуют"

    lines = ["📊 *Успеваемость:*"]
    for g in grades:
        subject = g.get("subject", "")
        grade = g.get("grade", "")
        lines.append(f"{subject}: {grade}")

    return "\n".join(lines)


def format_attendance_message(data: dict) -> str:
    """
    Форматирование посещаемости
    """
    payload = data.get("data") or {}
    attendance = payload.get("attendance")

    if not attendance:
        return "Данные о посещаемости отсутствуют"

    lines = ["📋 *Посещаемость:*"]
    for row in attendance:
        date = row.get("date", "")
        discipline = row.get("discipline", "")
        present = row.get("present", False)
        mark = "✅ присутствовал" if present else "❌ отсутствовал"
        lines.append(f"{date} — {discipline}: {mark}")

    return "\n".join(lines)
