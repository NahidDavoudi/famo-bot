"""Main application entry point (Famo bot)."""

from flask import Flask
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

import handlers.keyboards as kb
from config import config
from logging_config import logger
from event_loop import run_async
from handlers import buttons, commands, messages
from webhook import register_webhook_routes

app = Flask(__name__)

ptb_app = Application.builder().token(config.BOT_TOKEN).updater(None).build()

ptb_app.add_handler(CommandHandler("start", commands.start))
ptb_app.add_handler(CommandHandler("help", commands.help_command))
ptb_app.add_handler(CallbackQueryHandler(buttons.on_callback))
ptb_app.add_handler(MessageHandler(filters.CONTACT, messages.on_contact))

_menu_texts = "|".join([kb.BTN_WEEK, kb.BTN_HELP, kb.BTN_INBOX, kb.BTN_BROADCAST, kb.BTN_SIGNUP])
ptb_app.add_handler(MessageHandler(filters.Regex(f"^({_menu_texts})$"), messages.menu_button))
ptb_app.add_handler(MessageHandler(~filters.COMMAND, messages.on_message))
ptb_app.add_error_handler(messages.on_error)

run_async(ptb_app.initialize())
logger.info("Telegram Application با موفقیت مقداردهی اولیه شد")

register_webhook_routes(app, ptb_app)


@app.route("/")
def index():
    return "ربات فامو فعال است ✅", 200
