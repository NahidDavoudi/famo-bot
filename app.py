"""Main application entry point.

Wires together:
- configuration (config.py)
- logging (logging_config.py)
- handlers (handlers/)
- webhook routes (webhook.py)
"""

import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from config import config
from logging_config import logger  # noqa: F401  (set up logging on import)
from handlers import commands, messages
from webhook import register_webhook_routes
from telegram.ext import CallbackQueryHandler
from handlers import buttons



# --- ساخت Flask ---
app = Flask(__name__)

# --- ساخت Telegram Application ---
ptb_app = (
    Application.builder()
    .token(config.BOT_TOKEN)
    .updater(None)          # چون از وبهوک استفاده می‌کنیم
    .build()
)

# --- ثبت هندلرها ---
ptb_app.add_handler(CommandHandler("start", commands.start))
ptb_app.add_handler(CommandHandler("help", commands.help_command))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages.echo))
ptb_app.add_handler(CommandHandler("menu", commands.menu))
ptb_app.add_handler(CallbackQueryHandler(buttons.menu_button, pattern="^menu_"))
ptb_app.add_handler(MessageHandler(
    filters.Regex("^(📊 آمار|❓ راهنما|📞 تماس با ما)$"),
    bottom_button_handler,
))

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)
_loop.run_until_complete(ptb_app.initialize())
logger.info("Telegram Application با موفقیت مقداردهی اولیه شد")


register_webhook_routes(app, ptb_app)
logger.info(f"روت‌های وبهوک ثبت شدند (مسیر: {config.WEBHOOK_PATH})")


@app.route("/")
def index():
    return "ربات فعال است ✅", 200