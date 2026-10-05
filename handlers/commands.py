"""Command handlers: /start, /help."""

from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from keyboards import main_menu_keyboard

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the main menu."""
    await update.message.reply_text(
        "منوی اصلی:",
        reply_markup=main_menu_keyboard(),
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"/start از کاربر {user.id} (@{user.username})")
    await update.message.reply_text(
        f"Hello {user.first_name}!\n"
        "Welcome to the famoacademies bot.\n"
        "To start using the bot, connect your account by clicking the button below.\n"
        "Press /help to see the help message."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"/help از کاربر {update.effective_user.id}")
    await update.message.reply_text(
        "📚 راهنما:\n"
        "/start - شروع\n"
        "/login - ورود به حساب کاربری\n"
        "/help - همین راهنما\n\n"
    )

    