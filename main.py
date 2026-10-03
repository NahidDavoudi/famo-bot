"""Bot entrypoint.

This module wires together:
- configuration (token loading)
- dispatcher + storage (FSM)
- routers (handlers)

Typical customization points for your own template-based bot:
- add more routers in `dp.include_routers(...)`
- swap `MemoryStorage()` for Redis storage in production
- configure logging level/format
- custom logging setup with the `logger` library (optional; aiogram provides good logging by default)
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from config_reader import config
from handlers import buttons, commands

# Basic logging so you can see incoming updates and errors in the console.
logging.basicConfig(level=logging.INFO)

# FSM storage keeps per-user/per-chat state for multi-step dialogs.
# `MemoryStorage` is fine for local development, but it resets on every restart.
storage = MemoryStorage()

async def main() -> None:
    """Start the bot using long polling.

Long polling is the simplest way to run a bot locally.
If you deploy via webhooks, remove `start_polling(...)` and configure webhook.
"""

    # Create bot client with the token loaded from `.env` (see `config_reader.py`).
    bot = Bot(token=config.bot_token.get_secret_value())

    # Dispatcher is the main routing engine: it receives updates and passes them
    # to the first handler that matches filters.
    dp = Dispatcher(storage=storage)

    # Attach routers with handlers.
    # Add your own routers here (e.g. `dp.include_routers(admin.router, ...)`).
    dp.include_routers(commands.router, buttons.router)

    # If the bot previously worked in webhook mode, remove webhook and optionally
    # drop pending updates so you start from a clean state.
    await bot.delete_webhook(drop_pending_updates=True)

    # Start receiving updates.
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Log the bot's startup.
    logger.info(f'Your bot is running!')
    # `asyncio.run` creates an event loop, runs `main()`, and closes the loop.
    asyncio.run(main())
    # Log the bot's shutdown.
    logger.info(f'Your bot is shutting down!')