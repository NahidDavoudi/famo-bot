"""Professional logging setup using loguru."""

import logging
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
    diagnose=False,
)

# --- ۲) فایل لاگ عمومی (چرخشی) ---
logger.add(
    LOG_DIR / "bot_{time:YYYY-MM-DD}.log",
    format=FILE_FORMAT,
    level=config.LOG_LEVEL,
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    backtrace=True,
    diagnose=False,
)

# --- ۳) فایل جداگانه فقط برای خطاها ---
logger.add(
    LOG_DIR / "errors_{time:YYYY-MM-DD}.log",
    format=FILE_FORMAT,
    level="ERROR",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)


# --- ۴) جایگزینی لاگر استاندارد پایتون با loguru ---
class InterceptHandler(logging.Handler):
    """Redirect stdlib logging records to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logged message originated
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(
    handlers=[InterceptHandler()],
    level=0,
    force=True,
)

__all__ = ["logger"]