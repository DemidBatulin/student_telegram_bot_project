
import sqlite3
from datetime import datetime

DB_NAME = "studentbot.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()


# ---------------- INIT ----------------

def init_db():
    # Студенты
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            ST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ST_TG_ID INTEGER UNIQUE NOT NULL,
            ST_CODE TEXT,
            ST_STATUS TEXT,
            ST_REGISTERED_AT TEXT,
            ST_PD_AGREEMENT INTEGER
        )
    """)

    # Запросы студентов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS StudentRequests (
            SR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ST_TG_ID INTEGER NOT NULL,
            SR_TYPE TEXT NOT NULL,
            SR_TEXT TEXT,
            SR_CREATED_AT TEXT,
            SR_STATUS TEXT
        )
    """)

    # Ответы на запросы
    cur.execute("""
        CREATE TABLE IF NOT EXISTS RequestAnswers (
            RA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            SR_ID INTEGER NOT NULL,
            RA_TEXT TEXT,
            RA_CREATED_AT TEXT
        )
    """)

    conn.commit()


# ---------------- STUDENT ----------------

def add_student(telegram_id: int):
    """
    Регистрирует студента по Telegram ID
    """
    cur.execute("""
        INSERT OR IGNORE INTO Students
        (ST_TG_ID, ST_STATUS, ST_REGISTERED_AT, ST_PD_AGREEMENT)
        VALUES (?, ?, ?, ?)
    """, (
        telegram_id,
        "активен",
        datetime.now().isoformat(),
        1
    ))
    conn.commit()


def bind_student_code(telegram_id: int, student_code: str):
    """
    Привязывает зачетную книжку к Telegram ID
    """
    cur.execute("""
        UPDATE Students
        SET ST_CODE = ?
        WHERE ST_TG_ID = ?
    """, (student_code, telegram_id))
    conn.commit()


def get_student_by_telegram(telegram_id: int):
    """
    Возвращает код зачетной книжки по Telegram ID
    """
    cur.execute("""
        SELECT ST_CODE
        FROM Students
        WHERE ST_TG_ID = ?
    """, (telegram_id,))
    row = cur.fetchone()
    return row["ST_CODE"] if row and row["ST_CODE"] else None


# ---------------- REQUESTS ----------------

def create_request(telegram_id: int, req_type: str, text: str = ""):
    cur.execute("""
        INSERT INTO StudentRequests
        (ST_TG_ID, SR_TYPE, SR_TEXT, SR_CREATED_AT, SR_STATUS)
        VALUES (?, ?, ?, ?, ?)
    """, (
        telegram_id,
        req_type,
        text,
        datetime.now().isoformat(),
        "новый"
    ))
    conn.commit()
    return cur.lastrowid


def save_answer(request_id: int, answer_text: str):
    cur.execute("""
        INSERT INTO RequestAnswers
        (SR_ID, RA_TEXT, RA_CREATED_AT)
        VALUES (?, ?, ?)
    """, (
        request_id,
        answer_text,
        datetime.now().isoformat()
    ))
    conn.commit()
