"""
config.py
---------
Central place for all settings: model name, temperature, and API key handling.
Keeping this separate means app.py never touches os.environ directly.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads a local .env file if present


class Settings:
    # Model + generation behavior
    MODEL_NAME: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0"))  # low = predictable, per spec

    # API key: prefer environment variable, fall back to None
    # (app.py will prompt the user for it in the sidebar if missing)
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    # Upload constraints
    MAX_PREVIEW_ROWS: int = 5
    ALLOWED_EXTENSIONS = (".csv",)


settings = Settings()