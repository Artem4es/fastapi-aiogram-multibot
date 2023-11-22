import asyncio
import logging
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler

from aiohttp import web
from aiohttp.web import _run_app
from fastapi import FastAPI

from src.app.schemas import BotData
from src.bots.db.crud import add_db_bot, db_bot_exists
from src.bots.db.database import get_async_session
from src.bots.main import main
from src.config import Settings

settings = Settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start bot app as a task. Activate main bot on first app start"""
    async for db_session in get_async_session():
        if not await db_bot_exists(settings.main_bot_token, db_session):
            main_bot_data = BotData(token=settings.main_bot_token, assistant_id=settings.main_bot_assistant_id)
            await add_db_bot(main_bot_data, db_session)

    bot_app: web.Application = main()
    asyncio.create_task(_run_app(bot_app, host=settings.bot_server_host, port=settings.bot_server_port))
    logger.info("Bot app coroutine has been created")
    yield


def setup_logging() -> None:
    handler = RotatingFileHandler("src/app/logs/app.log", maxBytes=5000000, backupCount=5)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[handler],
        encoding="utf-8",
    )
