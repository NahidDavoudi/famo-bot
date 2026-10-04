import os
import asyncio
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- تنظیمات ---
WEBHOOK_PATH = "/webhook_a1b2c3d4"
BASE_URL = "https://notification.nadlab.ir"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

ptb_app = (
    Application.builder()
    .token(os.getenv("BOT_TOKEN"))
    .updater(None)
    .build()
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من یک ربات ساده هستم. 👋")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"شما نوشتید: {update.message.text}")

ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)
_loop.run_until_complete(ptb_app.initialize())

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, ptb_app.bot)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(ptb_app.process_update(update))
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error processing update: {e}", exc_info=True)
    return "OK", 200

@app.route("/set_webhook")
def set_webhook():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        webhook_url = f"{BASE_URL}{WEBHOOK_PATH}"
        loop.run_until_complete(
            ptb_app.bot.set_webhook(
                url=webhook_url,
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        )
        return f"✅ وبهوک تنظیم شد: {webhook_url}", 200
    except Exception as e:
        return f"❌ خطا در تنظیم وبهوک: {e}", 500
    finally:
        loop.close()

@app.route("/")
def index():
    return "ربات فعال است ✅", 200