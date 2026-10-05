"""ارسال اعلان‌های صف‌شده بک‌اند (بدون cron: بعد از هر وبهوک اجرا می‌شود)."""

from loguru import logger

import api


async def drain(bot):
    try:
        items = await api.outbox_pending()
    except Exception as e:
        logger.warning(f"خواندن outbox ناموفق: {e}")
        return
    for it in items:
        try:
            await bot.send_message(it["chat_id"], it["text"])
            await api.outbox_ack(it["id"], ok=True)
        except Exception as e:
            logger.warning(f"ارسال outbox {it.get('id')} ناموفق: {e}")
            try:
                await api.outbox_ack(it["id"], ok=False)
            except Exception:
                pass
