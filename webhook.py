"""روت‌های وبهوک (با secret token و کلید ادمین)."""

import hmac

from flask import jsonify, request
from loguru import logger
from telegram import Update

import outbox
from config import config
from event_loop import run_async


def register_webhook_routes(app, ptb_app):
    def admin_ok() -> bool:
        return hmac.compare_digest(request.args.get("key", ""), config.ADMIN_KEY)

    @app.route(config.WEBHOOK_PATH, methods=["POST"])
    def webhook():
        token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not hmac.compare_digest(token, config.WEBHOOK_SECRET):
            return "forbidden", 403
        try:
            update = Update.de_json(request.get_json(force=True), ptb_app.bot)
            run_async(ptb_app.process_update(update))
        except Exception as e:
            logger.exception(f"خطا در پردازش آپدیت: {e}")
        try:
            run_async(outbox.drain(ptb_app.bot), timeout=60)
        except Exception as e:
            logger.exception(f"خطا در outbox: {e}")
        return "OK", 200

    @app.route("/set_webhook")
    def set_webhook():
        if not admin_ok():
            return "forbidden", 403
        try:
            url = f"{config.BASE_URL}{config.WEBHOOK_PATH}"
            run_async(ptb_app.bot.set_webhook(
                url=url,
                secret_token=config.WEBHOOK_SECRET,
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
            ))
            logger.info(f"وبهوک تنظیم شد: {url}")
            return jsonify({"ok": True, "url": url}), 200
        except Exception as e:
            logger.exception(f"خطا در تنظیم وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route("/delete_webhook")
    def delete_webhook():
        if not admin_ok():
            return "forbidden", 403
        try:
            run_async(ptb_app.bot.delete_webhook(drop_pending_updates=True))
            return jsonify({"ok": True}), 200
        except Exception as e:
            logger.exception(f"خطا در حذف وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route("/webhook_info")
    def webhook_info():
        if not admin_ok():
            return "forbidden", 403
        try:
            info = run_async(ptb_app.bot.get_webhook_info())
            return jsonify({
                "url": info.url,
                "pending_update_count": info.pending_update_count,
                "last_error_date": str(info.last_error_date) if info.last_error_date else None,
                "last_error_message": info.last_error_message,
            }), 200
        except Exception as e:
            logger.exception(f"خطا در دریافت اطلاعات وبهوک: {e}")
            return jsonify({"ok": False, "error": str(e)}), 500
