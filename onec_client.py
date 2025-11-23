from typing import Optional, Dict, Any

import requests
from requests.auth import HTTPBasicAuth

from .config import ONEC_BASE_URL, ONEC_USER, ONEC_PASSWORD


def _auth() -> Optional[HTTPBasicAuth]:
    if ONEC_USER and ONEC_PASSWORD:
        return HTTPBasicAuth(ONEC_USER, ONEC_PASSWORD)
    return None


def get_student_debt(student_id: str) -> Optional[Dict[str, Any]]:
    """
    В текущей generic-версии:
    - если задан ONEC_BASE_URL, пробуем обратиться к /debt
    - если нет, возвращаем тестовые данные (заглушка)
    """
    if not ONEC_BASE_URL:
        # тестовые данные
        return {
            "success": True,
            "student": f"Студент {student_id}",
            "total_debt": 12000,
            "items": [
                {"name": "Обучение за 1 семестр 2024", "amount": 7000},
                {"name": "Обучение за 2 семестр 2024", "amount": 5000},
            ],
        }

    url = f"{ONEC_BASE_URL}/debt"
    try:
        resp = requests.get(url, params={"student_id": student_id}, auth=_auth(), timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        print("[get_student_debt] error, falling back to stub:", exc)
        return {
            "success": True,
            "student": f"Студент {student_id}",
            "total_debt": 0,
            "items": [],
        }


def get_student_schedule(student_id: str) -> Optional[Dict[str, Any]]:
    """
    Generic-версия:
    - если нет 1С, возвращаем простое тестовое расписание
    - с 1С — обращаемся к /schedule
    """
    if not ONEC_BASE_URL:
        return {
            "success": True,
            "student": f"Студент {student_id}",
            "days": [
                {
                    "date": "2025-11-22",
                    "items": [
                        {"time": "09:00", "subject": "Математика", "room": "Ауд. 101"},
                        {"time": "11:00", "subject": "Информатика", "room": "Ауд. 202"},
                    ],
                }
            ],
        }

    url = f"{ONEC_BASE_URL}/schedule"
    try:
        resp = requests.get(url, params={"student_id": student_id}, auth=_auth(), timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        print("[get_student_schedule] error, falling back to stub:", exc)
        return {
            "success": True,
            "student": f"Студент {student_id}",
            "days": [],
        }
