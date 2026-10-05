import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central configuration object."""

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    BASE_URL: str = os.getenv("BASE_URL", "").rstrip("/")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")
    ADMIN_KEY: str = os.getenv("ADMIN_KEY", "")
    API_BASE_URL: str = os.getenv(
        "API_BASE_URL", "https://api.famoacademy.ir/api/v1"
    ).rstrip("/")
    API_KEY: str = os.getenv("API_KEY", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")



config = Config()
