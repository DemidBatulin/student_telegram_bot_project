from typing import Dict, List


def format_debt_message(data: Dict) -> str:
    if not data.get("items"):
        return "Задолженностей не обнаружено 🎉"

    lines: List[str] = []
    student = data.get("student") or "студент"
    lines.append(f"Задолженности {student}:")
    total = data.get("total_debt", 0)

    for item in data["items"]:
        name = item.get("name", "Статья")
        amount = item.get("amount", 0)
        lines.append(f"• {name}: {amount} руб.")

    lines.append(f"
Итого: {total} руб.")
    return "
".join(lines)


def format_schedule_message(data: Dict) -> str:
    days = data.get("days") or []
    if not days:
        return "Расписание не найдено."

    lines: List[str] = []
    student = data.get("student") or "студент"
    lines.append(f"Расписание для {student}:")

    for day in days:
        date = day.get("date", "Дата")
        lines.append(f"
📅 {date}")
        for item in day.get("items") or []:
            time = item.get("time", "--:--")
            subject = item.get("subject", "Предмет")
            room = item.get("room", "аудитория не указана")
            lines.append(f"– {time} {subject} ({room})")

    return "
".join(lines)
