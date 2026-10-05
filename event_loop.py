"""Shared asyncio event loop for the whole application.

Passenger/WSGI برای هر درخواست یک context جدید می‌سازد، اما کلاینت httpx
داخل python-telegram-bot به یک حلقه رویداد مشخص گره می‌خورد. پس باید
یک حلقه پایدار در یک ترد پس‌زمینه داشته باشیم و همه coroutineها را به آن بسپاریم.
"""

import asyncio
import threading
from loguru import logger


# --- ساخت حلقه رویداد مشترک ---
_loop = asyncio.new_event_loop()


def _start_loop() -> None:
    """اجرای حلقه در ترد پس‌زمینه."""
    asyncio.set_event_loop(_loop)
    _loop.run_forever()


_thread = threading.Thread(
    target=_start_loop,
    daemon=True,
    name="bot-event-loop",
)
_thread.start()
logger.info("✅ حلقه رویداد پس‌زمینه راه‌اندازی شد")


def run_async(coro, timeout: float = 30.0):
    """ارسال یک coroutine به حلقه مشترک و انتظار برای نتیجه.

    Parameters
    ----------
    coro : Coroutine
        coroutine مورد نظر.
    timeout : float
        حداکثر زمان انتظار (ثانیه).
    """
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result(timeout=timeout)