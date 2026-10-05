from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo any text message back to the user."""
    text = update.message.text
    user = update.effective_user
    logger.debug(f"پیام از {user.id}: {text[:50]}")
    await update.message.reply_text(f"شما نوشتید: {text}")


async def bottom_button_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle clicks on the bottom (reply) keyboard buttons."""
    text = update.message.text
    logger.info(f"دکمه پایین: {text} از کاربر {update.effective_user.id}")

    if text == "📊 آمار":
        await update.message.reply_text("📊 ربات در حال اجراست ✅")
    elif text == "❓ راهنما":
        await update.message.reply_text(
            "📚 راهنما:\n"
            "/start - شروع\n"
            "/help - راهنما\n"
            "/menu - منو"
        )
    elif text == "📞 تماس با ما":
        await update.message.reply_text("📞 برای تماس: support@nadlab.ir")