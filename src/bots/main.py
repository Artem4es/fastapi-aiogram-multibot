import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
    setup_application,
)
from aiohttp import web

from src.bots.db.redis_config import storage
from src.bots.handlers import main_bot_router, multi_bot_router
from src.config import Settings

logger = logging.getLogger(__name__)

settings = Settings()


async def on_startup(bot: Bot):
    await bot.set_webhook(f"{settings.base_webhook_url}{settings.main_bot_path}")
    commands = [
        BotCommand(command="start", description="🧑‍💻 Начать диалог"),
        BotCommand(command="refresh_history", description="📜 Обновить историю чата"),
    ]
    await bot.set_my_commands(commands)


def main() -> web.Application:
    bot = Bot(token=settings.main_bot_token)

    main_dispatcher = Dispatcher(storage=storage)

    main_dispatcher.include_router(main_bot_router)
    main_dispatcher.startup.register(on_startup)

    multibot_dispatcher = Dispatcher(storage=storage)
    multibot_dispatcher.include_router(multi_bot_router)

    bot_app = web.Application()

    SimpleRequestHandler(dispatcher=main_dispatcher, bot=bot).register(bot_app, path=settings.main_bot_path)
    TokenBasedRequestHandler(dispatcher=multibot_dispatcher).register(bot_app, path=settings.other_bots_path)

    setup_application(bot_app, main_dispatcher, bot=bot)
    setup_application(bot_app, multibot_dispatcher)
    return bot_app


def setup_logging() -> None:
    handler = RotatingFileHandler("src/bots/logs/bots.log", maxBytes=5000000, backupCount=5)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[handler],
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        app: web.Application = main()
        setup_logging()
        logger.info("Bot app has been started...")
        web.run_app(app, host=settings.bot_server_host, port=settings.bot_server_port)

    except Exception as e:
        logger.error(e, exc_info=True)
        raise e

    finally:
        logger.info("Bot app has been STOPPED.")
