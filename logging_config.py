"""Professional logging setup using loguru.

Features:
- Colored console output for development
- Rotating file logs (10 MB per file)
- Automatic compression of old logs (zip)
- 7-day retention
- Separate error log file
- Structured format with timestamp, level, module, function, line
"""

import sys
from pathlib import Path
from loguru import logger

from config import config


# --- مسیر پوشه لاگ‌ها ---
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# --- حذف هندلر پیش‌فرض loguru ---
logger.remove()

# --- قالب‌بندی خروجی ---
CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "{level: <8} | "
    "{name}:{function}:{line} | "
    "{message}"
)

# --- ۱) خروجی کنسول (رنگی) ---
logger.add(
    sys.stderr,
    format=CONSOLE_FORMAT,
    level=config.LOG_LEVEL,
    colorize=True,
    backtrace=True,
    diagnose=False,   # در پروداکشن False باشد تا اطلاعات حساس لو نرود
)

# --- ۲) فایل لاگ عمومی (چرخشی) ---
logger.add(
    LOG_DIR / "bot_{time:YYYY-MM-DD}.log",
    format=FILE_FORMAT,
    level=config.LOG_LEVEL,
    rotation="10 MB",       # هر فایل حداکثر ۱۰ مگابایت
    retention="7 days",     # نگه‌داری ۷ روز
    compression="zip",      # فشرده‌سازی فایل‌های قدیمی
    encoding="utf-8",
    enqueue=True,           # ایمن برای چند ترد
    backtrace=True,
    diagnose=False,
)

# --- ۳) فایل جداگانه فقط برای خطاها ---
logger.add(
    LOG_DIR / "errors_{time:YYYY-MM-DD}.log",
    format=FILE_FORMAT,
    level="ERROR",
    rotation="10 MB",
    retention="30 days",    # خطاها بیشتر نگه‌داری شوند
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    backtrace=True,
    diagnose=True,          # در فایل خطا، جزئیات بیشتر مفید است
)

# --- ۴) جایگزینی لاگر استاندارد پایتون با loguru ---
class InterceptHandler:
    """Redirect stdlib logging to loguru."""

    @staticmethod
    def emit(record) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == __file__:
            frame = frame.f_back
            depth -= 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


import logging  # noqa: E402

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

# لاگر آماده برای import در سایر ماژول‌ها
__all__ = ["logger"]