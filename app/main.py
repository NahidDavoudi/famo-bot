import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import FastAPI, Header, HTTPException, Request

from . import config
from .handlers import router

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")

dp = Dispatcher()
dp.include_router(router)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/")
async def health():
    return {"ok": True}


@app.post(config.WEBHOOK_PATH)
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if x_telegram_bot_api_secret_token != config.WEBHOOK_SECRET:
        raise HTTPException(status_code=403)

    # روی cPanel (Passenger/WSGI) هر درخواست حلقه‌ی asyncio جدا می‌گیره،
    # برای همین Bot رو برای هر درخواست می‌سازیم و آخرش می‌بندیم.
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    try:
        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception:
        log.exception("update failed")
    finally:
        await bot.session.close()

    # همیشه 200 برمی‌گردونیم تا تلگرام آپدیت رو بی‌نهایت دوباره نفرسته
    return {"ok": True}
