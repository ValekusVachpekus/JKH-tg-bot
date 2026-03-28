import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
DB_PATH: str = os.getenv("DB_PATH", "data/complaints.db")
LOG_CHAT_ID: int = int(os.getenv("LOG_CHAT_ID", "0"))
MEDIA_DIR: Path = Path("data/media")
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
