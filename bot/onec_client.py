import requests
from urllib.parse import urljoin

from config import ONEC_BASE_URL, ONEC_USER, ONEC_PASSWORD, ONEC_TIMEOUT


def _call_1c(method: str, params: dict | None = None) -> dict:
    """
    Унифицированный вызов HTTP-сервиса 1С.
    ONEC_BASE_URL должен указывать на базовый адрес сервиса, например:
    http://localhost/yourbase/hs/StudentInfo/
    """
    if not ONEC_BASE_URL:
        return {"success": False, "error": "ONEC_BASE_URL is not set"}

    url = urljoin(ONEC_BASE_URL.rstrip("/") + "/", method.lstrip("/"))

    try:
        resp = requests.get(
            url,
            params=params or {},
            auth=(ONEC_USER, ONEC_PASSWORD) if ONEC_USER else None,
            timeout=ONEC_TIMEOUT,
        )

        # 1С часто возвращает JSON строкой
        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {resp.status_code}",
                "details": resp.text[:300],
                "url": url,
            }

        try:
            data = resp.json()
        except Exception:
            return {
                "success": False,
                "error": "Invalid JSON from 1C",
                "details": resp.text[:300],
                "url": url,
            }

        # если 1С вернула {"error": "..."} — пробрасываем
        if isinstance(data, dict) and data.get("error"):
            return {"success": False, "error": data.get("error"), "data": data}

        return {"success": True, "data": data}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Connection error", "details": str(e), "url": url}


# ---------------- PUBLIC API for bot ----------------

def get_debt(student_code: str) -> dict:
    # В 1С ты добавила метод GetDebt — используем его
    return _call_1c("GetDebt", {"student_id": student_code})


def get_schedule(student_code: str) -> dict:
    return _call_1c("GetSchedule", {"student_id": student_code})


def get_progress(student_code: str) -> dict:
    return _call_1c("GetProgress", {"student_id": student_code})


def get_attendance(student_code: str) -> dict:
    return _call_1c("GetAttendance", {"student_id": student_code})


def register_student(student_code: str, telegram_id: int) -> dict:
    # если у тебя в 1С есть RegisterStudent
    return _call_1c("RegisterStudent", {"student_id": student_code, "tg_id": telegram_id})
