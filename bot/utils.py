def format_debt_message(data):
    return (
        "📄 *Задолженность по оплате*\n\n"
        f"Сумма: {data['amount']} {data['currency']}"
    )


def format_schedule_message(data):
    text = "📅 *Расписание занятий*\n\n"
    for row in data["schedule"]:
        text += f"• {row}\n"
    return text
