from telegram import Update
from telegram.ext import ContextTypes

import api
import keyboards as kb
from handlers import commands, messages


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    action, _, arg = q.data.partition(":")
    chat_id = q.from_user.id
    ud = context.user_data

    # --- ثبت‌نام ---
    if action == "grade" and ud.get("state") == "signup_grade":
        ud.update(grade=arg, state="signup_major")
        await q.edit_message_text("رشته‌ات؟", reply_markup=kb.majors())
        return
    if action == "major" and ud.get("state") == "signup_major":
        user = await api.register(
            chat_id, ud["full_name"], ud["grade"], arg, ud.get("phone", "")
        )
        ud.clear()
        await q.edit_message_text("ثبت‌نام انجام شد ✅")
        await commands.show_home(q.message, user)
        return

    # --- پشتیبان ---
    user = await api.get_user(chat_id)
    if not user or user["role"] not in kb.STAFF:
        return

    if action == "inbox":
        await messages.send_inbox(q.edit_message_text, chat_id)
    elif action == "thread":
        t = await api.thread(chat_id, arg)
        lines = []
        for m in t["messages"][-10:]:
            who = {"student": "🧑‍🎓", "supporter": "🧑‍🏫", "broadcast": "📣 همگانی"}.get(m["from"], "")
            lines.append(f"{who} {m.get('text') or ''}" + (" 📎" if m.get("has_file") else ""))
        await q.edit_message_text(
            f"{t['title']}\n\n" + "\n\n".join(lines), reply_markup=kb.thread_actions(arg)
        )
    elif action == "reply":
        ud.update(state="reply", thread_id=arg)
        await q.message.reply_text("پاسخت رو بفرست (متن یا فایل):")
    elif action == "bc":
        ud.update(state="broadcast", scope=arg)
        await q.edit_message_text("متن پیام همگانی رو بفرست (متن یا فایل):")
