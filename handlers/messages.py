from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

import api
import keyboards as kb
from handlers import commands

MAX_FILE = 20 * 1024 * 1024  # سقف دانلود بات‌ها در تلگرام


async def extract(msg):
    """متن + (اختیاری) فایل پیام را برای ارسال به API آماده می‌کند."""
    text = msg.text or msg.caption or ""
    obj = name = mime = None
    if msg.document:
        obj, name, mime = msg.document, msg.document.file_name, msg.document.mime_type
    elif msg.photo:
        obj, name, mime = msg.photo[-1], "photo.jpg", "image/jpeg"
    elif msg.voice:
        obj, name, mime = msg.voice, "voice.ogg", "audio/ogg"
    elif msg.video:
        obj, name, mime = msg.video, msg.video.file_name or "video.mp4", msg.video.mime_type
    elif msg.audio:
        obj, name, mime = msg.audio, msg.audio.file_name or "audio.mp3", msg.audio.mime_type
    file = None
    if obj:
        if obj.file_size and obj.file_size > MAX_FILE:
            raise ValueError("حجم فایل بیشتر از ۲۰ مگابایته")
        f = await obj.get_file()
        data = bytes(await f.download_as_bytearray())
        file = (name or "file", data, mime or "application/octet-stream")
    return text, file


async def _ack(msg):
    try:
        await msg.set_reaction("👍")
    except Exception:
        await msg.reply_text("✅ ثبت شد")


# ---------- شماره تماس ----------
async def on_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg.contact.user_id != update.effective_user.id:
        await msg.reply_text("لطفاً شماره‌ی خودت رو با دکمه بفرست.")
        return
    phone = msg.contact.phone_number
    user = await api.link_phone(update.effective_chat.id, phone)
    if user:
        await commands.show_home(msg, user)
        return
    context.user_data.update(state="signup_name", phone=phone)
    await msg.reply_text("حسابی با این شماره پیدا نشد. ثبت‌نام می‌کنیم.\nنام و نام خانوادگی‌ات؟")


# ---------- دکمه‌های منوی پایین ----------
async def menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg, text = update.message, update.message.text
    chat_id = update.effective_chat.id

    if text == kb.BTN_SIGNUP:
        if await api.get_user(chat_id):
            await commands.start(update, context)
            return
        context.user_data.update(state="signup_name", phone="")
        await msg.reply_text("نام و نام خانوادگی‌ات؟")
        return

    user = await api.get_user(chat_id)
    if not user:
        await commands.start(update, context)
        return
    staff = user["role"] in kb.STAFF
    context.user_data.pop("state", None)

    if text == kb.BTN_HELP:
        await msg.reply_text(commands.HELP_STAFF if staff else commands.HELP_STUDENT)
    elif text == kb.BTN_WEEK and not staff:
        data = await api.week_report(chat_id)
        lines = [f"{'✅' if d['sent'] else '⬜️'} {d['label']}" for d in data["days"]]
        await msg.reply_text(
            "گزارش این هفته:\n" + "\n".join(lines)
            + f"\n\n{data['sent_count']} روز از {len(lines)} روز"
        )
    elif text == kb.BTN_INBOX and staff:
        await send_inbox(msg.reply_text, chat_id)
    elif text == kb.BTN_BROADCAST and staff:
        await msg.reply_text("پیام برای چه کسانی ارسال بشه؟", reply_markup=kb.broadcast_scopes())


async def send_inbox(send, chat_id):
    from telegram import InlineKeyboardButton as IB, InlineKeyboardMarkup

    items = await api.inbox(chat_id)
    if not items:
        await send("صندوق ورودی خالیه ✨")
        return
    rows = [
        [IB(f"{t['student_name']}" + (f" ({t['unread']})" if t.get("unread") else ""),
            callback_data=f"thread:{t['thread_id']}")]
        for t in items
    ]
    await send("گزارش‌های امروز:", reply_markup=InlineKeyboardMarkup(rows))


# ---------- پیام‌های آزاد (ثبت‌نام / گزارش / پاسخ / همگانی) ----------
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    chat_id = update.effective_chat.id
    ud = context.user_data
    state = ud.get("state")

    # --- ثبت‌نام ---
    if state == "signup_name":
        name = (msg.text or "").strip()
        if len(name) < 3:
            await msg.reply_text("نام کامل رو بنویس (حداقل ۳ حرف).")
            return
        ud.update(full_name=name, state="signup_grade")
        await msg.reply_text("پایه‌ات؟", reply_markup=kb.grades())
        return
    if state in ("signup_grade", "signup_major"):
        await msg.reply_text("لطفاً از دکمه‌های بالا انتخاب کن 👆")
        return

    user = await api.get_user(chat_id)
    if not user:
        await commands.start(update, context)
        return
    staff = user["role"] in kb.STAFF

    try:
        text, file = await extract(msg)
    except ValueError as e:
        await msg.reply_text(str(e))
        return

    # --- پشتیبان: پاسخ به یک تردِ مشخص ---
    if staff and state == "reply":
        await api.send_reply(chat_id, ud["thread_id"], text, file)
        ud.pop("state", None)
        await _ack(msg)
        return

    # --- پشتیبان: پیام همگانی ---
    if staff and state == "broadcast":
        res = await api.broadcast(chat_id, ud["scope"], text, file)
        ud.pop("state", None)
        await msg.reply_text(f"✅ برای {res.get('recipients', 0)} نفر ارسال شد.")
        return

    # --- دانش‌آموز: هر پیام = بخشی از گزارش امروز ---
    if not staff:
        await api.send_report(chat_id, text, file)
        await _ack(msg)
        return

    await msg.reply_text("از منوی پایین یکی رو انتخاب کن 👇")


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.opt(exception=context.error).error("خطا در هندلر")
    if isinstance(update, Update) and update.effective_chat:
        try:
            await context.bot.send_message(
                update.effective_chat.id, "یه مشکلی پیش اومد، چند لحظه بعد دوباره امتحان کن 🙏"
            )
        except Exception:
            pass
