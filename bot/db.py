
import sqlite3
from datetime import datetime

DB_NAME = "studentbot.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()


def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        ST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ST_TG_ID INTEGER UNIQUE,
        ST_CODE TEXT UNIQUE,
        ST_STATUS TEXT,
        ST_REGISTERED_AT TEXT,
        ST_PD_AGREEMENT INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS StudentRequests (
        SR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ST_TG_ID INTEGER,
        SR_TYPE TEXT,
        SR_TEXT TEXT,
        SR_CREATED_AT TEXT,
        SR_STATUS TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS RequestAnswers (
        RA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SR_ID INTEGER,
        RA_TEXT TEXT,
        RA_CREATED_AT TEXT
    )
    """)

    conn.commit()


# ---------- STUDENTS ----------

def get_student_by_telegram(tg_id: int):
    cur.execute(
        "SELECT * FROM Students WHERE ST_TG_ID = ?",
        (tg_id,)
    )
    return cur.fetchone()


def add_student(tg_id: int, student_code: str):
    cur.execute("""
        INSERT OR IGNORE INTO Students
        (ST_TG_ID, ST_CODE, ST_STATUS, ST_REGISTERED_AT, ST_PD_AGREEMENT)
        VALUES (?, ?, ?, ?, ?)
    """, (
        tg_id,
        student_code,
        "активен",
        datetime.now().isoformat(),
        1
    ))
    conn.commit()


# ---------- REQUESTS ----------

def create_request(tg_id: int, req_type: str, text: str):
    cur.execute("""
        INSERT INTO StudentRequests
        (ST_TG_ID, SR_TYPE, SR_TEXT, SR_CREATED_AT, SR_STATUS)
        VALUES (?, ?, ?, ?, ?)
    """, (
        tg_id,
        req_type,
        text,
        datetime.now().isoformat(),
        "новый"
    ))
    conn.commit()
    return cur.lastrowid


def save_answer(request_id: int, text: str):
    cur.execute("""
        INSERT INTO RequestAnswers
        (SR_ID, RA_TEXT, RA_CREATED_AT)
        VALUES (?, ?, ?)
    """, (
        request_id,
        text,
        datetime.now().isoformat()
    ))
    conn.commit()
