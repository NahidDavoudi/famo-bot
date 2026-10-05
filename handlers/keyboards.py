from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup


def bottom_menu_keyboard() -> ReplyKeyboardMarkup:
    """Persistent bottom keyboard."""
    keyboard = [
        [KeyboardButton("📊 آمار"), KeyboardButton("❓ راهنما")],
        [KeyboardButton("📞 تماس با ما")],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,   # همیشه نمایش داده شود
        input_field_placeholder="یک گزینه انتخاب کنید...",
    )

def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📊 آمار", callback_data="menu_stats"),
            InlineKeyboardButton("❓ راهنما", callback_data="menu_help"),
        ],
        [
            InlineKeyboardButton("🌐 وب‌سایت", url="https://nadlab.ir"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)