import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/complaints.db")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
MEDIA_DIR = Path("data/media")
