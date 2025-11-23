import sqlite3
from pathlib import Path
from typing import Optional, List, Dict

from .config import SQLITE_DB_PATH, BASE_DIR


def _db_path() -> Path:
    p = Path(SQLITE_DB_PATH)
    if not p.is_absolute():
        p = BASE_DIR / p
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            group_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS student_links (
            telegram_id INTEGER PRIMARY KEY,
            student_id TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        """
    )

    conn.commit()
    conn.close()


def add_student(student_id: str, full_name: str, group_name: str = "") -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO students (id, full_name, group_name)
        VALUES (?, ?, ?)
        """,
        (student_id, full_name, group_name),
    )
    conn.commit()
    conn.close()


def list_students() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, group_name, created_at FROM students ORDER BY full_name")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def bind_student(telegram_id: int, student_id: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO student_links (telegram_id, student_id)
        VALUES (?, ?)
        """,
        (telegram_id, student_id),
    )
    conn.commit()
    conn.close()


def get_student_id_by_telegram(telegram_id: int) -> Optional[str]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id FROM student_links WHERE telegram_id = ?", (telegram_id,))
    row = cur.fetchone()
    conn.close()
    return row["student_id"] if row else None


def list_bindings() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sl.telegram_id, sl.student_id, sl.created_at,
               s.full_name, s.group_name
        FROM student_links sl
        LEFT JOIN students s ON s.id = sl.student_id
        ORDER BY sl.created_at DESC
        """
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
