import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

ENV = os.getenv("ENV", "dev")
BASE_DIR = Path(__file__).resolve().parents[2]

ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DB_PATH = (BASE_DIR / "test.db").resolve().as_posix()
DB_URL = os.getenv("DB_URL", f"sqlite:///{DB_PATH}")

if DB_URL.strip().lower() == "sqlite":
    DB_URL = f"sqlite:///{DB_PATH}"

CACHE_HOST = os.getenv("CACHE_HOST", "localhost")
CACHE_PORT = int(os.getenv("CACHE_PORT", 11211))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

ALLOWED_PAIRS: List[str] = os.getenv("ALLOWED_PAIRS", "BRLBTC,BRLETH").split(",")
MB_API_BASE_URL = os.getenv("MB_API_BASE_URL", "https://mobile.mercadobitcoin.com.br")
