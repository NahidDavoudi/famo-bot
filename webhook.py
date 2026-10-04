"""Webhook blueprint.

All webhook-related routes live here, separate from the main app.
"""

import asyncio
from flask import Blueprint, request, jsonify
from telegram import Update
from loguru import logger

from config import config


# Blueprint فقط برای منطق وبهوک
webhook_bp = Blueprint("webhook", __name__)


def _run_async(coro):
    """اجرای یک coroutine در یک حلقه رویداد جدید (سازگار با Passenger/WSGI)."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def register_webhook_routes(app, ptb_app):
    """ثبت روت‌های وبهوک روی Flask app و اتصال به PTB Application.

    Parameters
    ----------
    app : flask.Flask
        اپلیکیشن Flask اصلی.
    ptb_app : telegram.ext.Application
        اپلیکیشن python-telegram-bot.
    """

    # --- دریافت آپدیت از تلگرام ---
    @app.route(config.WEBHOOK_PATH, methods=["POST"])
    def webhook():
        try:
            data = request.get_json(force=True)
            update = Update.de_json(data, ptb_app.bot)
            _run_async(ptb_app.process_update(update))
        except Exception as e:
            logger.exception(f"خطا در پردازش آپدیت: {e}")
        return "OK", 200

    # --- تنظیم وبهوک ---
    @app.route("/set_webhook")
    def set_webhook():
        try:
            webhook_url = f"{config.BASE_URL}{config.WEBHOOK_PATH}"
            _run_async(
                ptb_app.bot.set_webhook(
                    url=webhook_url,
                    allowed_updates=Update.ALL_TYPES,
                    drop_pending_updates=True,
                )
            )
            logger.info(f"وبهوک تنظیم شد: {webhook_url}")
            return jsonify({
                "ok": True,
                "message": f"وبهوک تنظیم شد: {webhook_url}",
            }), 200
        except Exception as e:
            logger.exception(f"خطا در تنظیم وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500

    # --- حذف وبهوک (برای زمانی که می‌خواهید ربات را از حالت وبهوک دربیاورید) ---
    @app.route("/delete_webhook")
    def delete_webhook():
        try:
            _run_async(ptb_app.bot.delete_webhook(drop_pending_updates=True))
            logger.info("وبهوک حذف شد")
            return jsonify({"ok": True, "message": "وبهوک حذف شد"}), 200
        except Exception as e:
            logger.exception(f"خطا در حذف وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500

    # --- وضعیت وبهوک ---
    @app.route("/webhook_info")
    def webhook_info():
        try:
            info = _run_async(ptb_app.bot.get_webhook_info())
            return jsonify({
                "url": info.url,
                "pending_update_count": info.pending_update_count,
                "last_error_date": str(info.last_error_date) if info.last_error_date else None,
                "last_error_message": info.last_error_message,
            }), 200
        except Exception as e:
            logger.exception(f"خطا در دریافت اطلاعات وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500