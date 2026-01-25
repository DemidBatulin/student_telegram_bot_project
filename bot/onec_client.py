# onec_client.py
import requests
from typing import Optional

# Адрес HTTP-сервиса 1С
ONEC_BASE_URL = "http://localhost/StudentBotAPI/hs"

# Если в 1С включена авторизация
ONEC_USER = "bot_user"
ONEC_PASSWORD = "password"


def _call_1c(method: str, payload: dict) -> Optional[dict]:
    """
    Универсальный вызов HTTP-сервиса 1С
    """
    url = f"{ONEC_BASE_URL}/{method}"
    try:
        response = requests.post(
            url,
            json=payload,
            auth=(ONEC_USER, ONEC_PASSWORD),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[1C ERROR] {method}: {e}")
        return None


def get_student_debt(student_id: str) -> Optional[dict]:
    """
    Получение задолженности студента из 1С
    """
    return _call_1c(
        "GetStudentDebt",
        {"StudentID": student_id}
    )


def get_student_schedule(student_id: str) -> Optional[dict]:
    """
    Получение расписания студента из 1С
    """
    return _call_1c(
        "GetStudentSchedule",
        {"StudentID": student_id}
    )


def register_request_in_1c(request_id: int, student_id: str, request_type: str):
    """
    Регистрация обращения в 1С
    """
    return _call_1c(
        "RegisterRequest",
        {
            "RequestID": request_id,
            "StudentID": student_id,
            "RequestType": request_type
        }
    )
