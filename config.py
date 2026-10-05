import os
from dotenv import load_dotenv

# Load variables from .env into os.environ (only if not already set)
load_dotenv()


class Config:
    """Central configuration object."""

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")
    BASE_URL: str = os.getenv("BASE_URL", "").rstrip("/")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        """Ensure required settings exist before the app starts."""
        missing = []
        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        if not cls.BASE_URL:
            missing.append("BASE_URL")
        if missing:
            raise ValueError(
                f"متغیرهای محیطی زیر تنظیم نشده‌اند: {', '.join(missing)}"
            )


config = Config()
config.validate()