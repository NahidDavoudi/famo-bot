"""Non-command message handlers."""

from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo any text message back to the user."""
    text = update.message.text
    user = update.effective_user
    logger.debug(f"پیام از {user.id}: {text[:50]}")
    await update.message.reply_text(f"شما نوشتید: {text}")