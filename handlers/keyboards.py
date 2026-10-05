from telegram import (
    InlineKeyboardButton as IB,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

BTN_WEEK = "📊 گزارش هفته"
BTN_HELP = "❓ راهنما"
BTN_INBOX = "📥 صندوق ورودی"
BTN_BROADCAST = "📣 پیام همگانی"
BTN_SIGNUP = "✍️ ثبت‌نام در ربات"

STAFF = ("supporter", "admin")

GRADES = {"10": "دهم", "11": "یازدهم", "12": "دوازدهم", "grad": "فارغ‌التحصیل"}
MAJORS = {"tajrobi": "تجربی", "riazi": "ریاضی", "ensani": "انسانی"}


def main_menu(role):
    if role in STAFF:
        rows = [[BTN_INBOX, BTN_BROADCAST], [BTN_HELP]]
    else:
        rows = [[BTN_WEEK, BTN_HELP]]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def start_menu():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📱 ارسال شماره من", request_contact=True)], [BTN_SIGNUP]],
        resize_keyboard=True,
    )


def grades():
    return InlineKeyboardMarkup(
        [[IB(v, callback_data=f"grade:{k}") for k, v in GRADES.items()]]
    )


def majors():
    return InlineKeyboardMarkup(
        [[IB(v, callback_data=f"major:{k}") for k, v in MAJORS.items()]]
    )


def broadcast_scopes():
    return InlineKeyboardMarkup([
        [IB("فقط بدون گزارش امروز", callback_data="bc:no_report")],
        [IB("همه دانش‌آموزان من", callback_data="bc:all")],
    ])


def thread_actions(thread_id):
    return InlineKeyboardMarkup([
        [IB("✉️ پاسخ", callback_data=f"reply:{thread_id}")],
        [IB("⬅️ بازگشت", callback_data="inbox:")],
    ])
