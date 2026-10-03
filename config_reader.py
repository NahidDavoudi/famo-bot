"""Application configuration.

The template reads configuration from environment variables and/or a local
`.env` file (not committed).

To run the bot, create `.env` with:
- BOT_TOKEN=123456:ABC-DEF...
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Typed settings loaded from environment variables.

    Pydantic will automatically map `bot_token` to `BOT_TOKEN` by default.
    """

    # Telegram bot token.
    # `SecretStr` prevents accidental token leaks via `repr()`/logs.
    bot_token: SecretStr

    class Config:
        # Load variables from `.env` in the project root for local development.
        env_file = ".env"
        env_file_encoding = "utf-8"


# A singleton config object imported across the project.
config = Settings()
