"""یک بار (و بعد از هر تغییر آدرس/توکن) اجرا کن: python set_webhook.py"""
import asyncio

from aiogram import Bot

from app import config
from app.main import dp


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    try:
        await bot.set_webhook(
            url=config.WEBHOOK_URL,
            secret_token=config.WEBHOOK_SECRET,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        info = await bot.get_webhook_info()
        print("Webhook:", info.url)
        print("Pending:", info.pending_update_count)
        print("Last error:", info.last_error_message)
    finally:
        await bot.session.close()


asyncio.run(main())
