from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle clicks on main menu inline buttons."""
    query = update.callback_query
    await query.answer()

    logger.info(f"کلیک روی {query.data} از کاربر {query.from_user.id}")

    if query.data == "menu_stats":
        await query.edit_message_text("📊 آمار ربات:\nربات در حال اجراست ✅")
    elif query.data == "menu_help":
        await query.edit_message_text(
            "📚 راهنما:\n"
            "/start - شروع\n"
            "/help - راهنما\n"
            "/menu - منو"
        )