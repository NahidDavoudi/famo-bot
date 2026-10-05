"""Webhook blueprint.

All webhook-related routes live here, separate from the main app.
"""

from flask import Blueprint, jsonify, request
from telegram import Update
from loguru import logger

from config import config
from event_loop import run_async          # ← جدید


webhook_bp = Blueprint("webhook", __name__)


def register_webhook_routes(app, ptb_app):
    """ثبت روت‌های وبهوک روی Flask app و اتصال به PTB Application."""

    @app.route(config.WEBHOOK_PATH, methods=["POST"])
    def webhook():
        try:
            data = request.get_json(force=True)
            update = Update.de_json(data, ptb_app.bot)
            run_async(ptb_app.process_update(update))   # ← حلقه مشترک
        except Exception as e:
            logger.exception(f"خطا در پردازش آپدیت: {e}")
        return "OK", 200

    @app.route("/set_webhook")
    def set_webhook():
        try:
            webhook_url = f"{config.BASE_URL}{config.WEBHOOK_PATH}"
            run_async(
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

    @app.route("/delete_webhook")
    def delete_webhook():
        try:
            run_async(ptb_app.bot.delete_webhook(drop_pending_updates=True))
            logger.info("وبهوک حذف شد")
            return jsonify({"ok": True, "message": "وبهوک حذف شد"}), 200
        except Exception as e:
            logger.exception(f"خطا در حذف وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route("/webhook_info")
    def webhook_info():
        try:
            info = run_async(ptb_app.bot.get_webhook_info())
            return jsonify({
                "url": info.url,
                "pending_update_count": info.pending_update_count,
                "last_error_date": (
                    str(info.last_error_date) if info.last_error_date else None
                ),
                "last_error_message": info.last_error_message,
            }), 200
        except Exception as e:
            logger.exception(f"خطا در دریافت اطلاعات وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500