from telegram import Update
from telegram.ext import ContextTypes

import api
from handlers import keyboeards as kb

HELP_STUDENT = (
    "هر پیام، عکس یا فایلی که اینجا بفرستی، به‌عنوان گزارش امروزت برای "
    "پشتیبانت ثبت می‌شه. جواب پشتیبان هم همین‌جا برات میاد.\n\n"
    "📊 گزارش هفته: روزهایی که گزارش دادی و ندادی"
)
HELP_STAFF = (
    "📥 صندوق ورودی: گزارش‌های دانش‌آموزان و پاسخ دادن\n"
    "📣 پیام همگانی: ارسال پیام به دانش‌آموزانت"
)


async def show_home(message, user):
    await message.reply_text(
        f"سلام {user['full_name']} 👋", reply_markup=kb.main_menu(user["role"])
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    user = await api.get_user(update.effective_chat.id)
    if user:
        await show_home(update.message, user)
        return
    await update.message.reply_text(
        "به ربات فامو خوش اومدی 🌱\n"
        "برای شروع، شماره‌ات رو بفرست تا حسابت پیدا بشه، یا ثبت‌نام کن.",
        reply_markup=kb.start_menu(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await api.get_user(update.effective_chat.id)
    text = HELP_STAFF if user and user["role"] in kb.STAFF else HELP_STUDENT
    await update.message.reply_text(text)
