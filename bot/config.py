import os
from pathlib import Path

from dotenv import load_dotenv

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем .env (если есть)
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

ONEC_BASE_URL = os.getenv("ONEC_BASE_URL", "").rstrip("/")
ONEC_USER = os.getenv("ONEC_USER", "").strip()
ONEC_PASSWORD = os.getenv("ONEC_PASSWORD", "").strip()

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/students.db")

if not TELEGRAM_BOT_TOKEN:
    print("WARNING: TELEGRAM_BOT_TOKEN is not set. Please configure it in .env.", flush=True)
