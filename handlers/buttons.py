from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from keyboards import bottom_menu_keyboard

async def menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle clicks on main menu buttons."""
    query = update.callback_query
    await query.answer()  # مهم: حتماً answer کنید تا دکمه از حالت لود خارج شود

    logger.info(f"کلیک روی {query.data} از کاربر {query.from_user.id}")

    if query.data == "menu_stats":
        await query.edit_message_text("📊 آمار ربات:\nربات در حال اجراست ✅")
    elif query.data == "menu_help":
        await query.edit_message_text(
            "📚 راهنما:\n"
            "/start - شروع\n"
            "/help - راهنما\n"
            "/stats - آمار"
        )

async def menu_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "منو فعال شد:",
        reply_markup=bottom_menu_keyboard(),
    )