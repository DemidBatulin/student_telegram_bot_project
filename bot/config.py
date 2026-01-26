import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

ONEC_BASE_URL = os.getenv("ONEC_BASE_URL", "")  # например: http://localhost/BASE/hs/StudentInfo/
ONEC_USER = os.getenv("ONEC_USER", "")          # если требуется
ONEC_PASSWORD = os.getenv("ONEC_PASSWORD", "")  # если требуется
ONEC_TIMEOUT = int(os.getenv("ONEC_TIMEOUT", "10"))
