"""Command handlers: /start, /help."""

from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"/start از کاربر {user.id} (@{user.username})")
    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\n"
        "من یک ربات ساده هستم.\n"
        "دستور /help را بزنید تا راهنما را ببینید."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    logger.info(f"/help از کاربر {update.effective_user.id}")
    await update.message.reply_text(
        "📚 راهنما:\n"
        "/start - شروع\n"
        "/help - همین راهنما\n\n"
        "هر پیام متنی بفرستید، آن را تکرار می‌کنم."
    )