import asyncio

from flask import Flask
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import config
from logging_config import logger  # noqa: F401
from handlers import buttons, commands, messages
from webhook import register_webhook_routes


# --- ساخت Flask ---
app = Flask(__name__)

# --- ساخت Telegram Application ---
ptb_app = (
    Application.builder()
    .token(config.BOT_TOKEN)
    .updater(None)
    .build()
)


# --- ثبت هندلرها (ترتیب مهم است) ---

# ۱) کامندها
ptb_app.add_handler(CommandHandler("start", commands.start))
ptb_app.add_handler(CommandHandler("help", commands.help_command))
ptb_app.add_handler(CommandHandler("menu", commands.menu))

# ۲) دکمه‌های شیشه‌ای (Inline)
ptb_app.add_handler(
    CallbackQueryHandler(buttons.menu_button, pattern="^menu_")
)

# ۳) دکمه‌های پایین صفحه (Reply) — قبل از echo
ptb_app.add_handler(
    MessageHandler(
        filters.Regex("^(📊 آمار|❓ راهنما|📞 تماس با ما)$"),
        messages.bottom_button_handler,
    )
)

# ۴) echo — عمومی‌ترین، آخر
ptb_app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, messages.echo)
)


# --- مقداردهی اولیه PTB ---
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)
_loop.run_until_complete(ptb_app.initialize())
logger.info("Telegram Application با موفقیت مقداردهی اولیه شد")


# --- روت‌های وبهوک ---
register_webhook_routes(app, ptb_app)
logger.info(f"روت‌های وبهوک ثبت شدند (مسیر: {config.WEBHOOK_PATH})")


# --- روت سلامت ---
@app.route("/")
def index():
    return "ربات فعال است ✅", 200