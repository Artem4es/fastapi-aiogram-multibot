import logging
from http import HTTPStatus
from typing import Optional

from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.utils.token import TokenValidationError
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas import BotData
from src.bots.db.crud import add_db_bot
from src.config import Settings

logger = logging.getLogger(__name__)

settings = Settings()

OTHER_BOTS_URL = f"{settings.base_webhook_url}{settings.other_bots_path}"


async def activate_bot(token: str) -> None:
    """Set token based webhook for new tg bot"""
    try:
        new_bot = Bot(token=token)

    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail={"status": "Error", "reason": "Invalid bot token"}
        )

    await new_bot.delete_webhook(drop_pending_updates=True)
    await new_bot.set_webhook(OTHER_BOTS_URL.format(bot_token=token))
    commands = [
        BotCommand(command="start", description="🧑‍💻 Начать диалог"),
        BotCommand(command="refresh_history", description="📜 Обновить историю чата"),
    ]
    await new_bot.set_my_commands(commands)


async def create_new_bot(bot_data: BotData, db_session: Optional[AsyncSession]) -> None:
    """Create new bot instance and write FSM state for that bot"""
    await activate_bot(bot_data.token)
    await add_db_bot(bot_data, db_session)
