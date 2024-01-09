import logging
from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.responses import activate_bot_resp, delete_bot_resp
from src.app.schemas import BotActivateResponse, BotData, Status, BaseBotData, BotDeleteResponse
from src.app.services import create_new_bot
from src.bots.core.managers import redis_storage_deletion_manager
from src.bots.db.crud import db_bot_exists, drop_db_bot
from src.bots.db.database import get_async_session

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/activate_bot", status_code=HTTPStatus.CREATED, name="Activate new bot in TG", responses=activate_bot_resp)
async def activate_bot(bot_data: BotData, db_session: Annotated[AsyncSession, Depends(get_async_session)]) -> BotActivateResponse:
    """Activate new tg bot using token"""
    try:
        if not await db_bot_exists(bot_data.token, db_session):
            await create_new_bot(bot_data, db_session)
            return BotActivateResponse(status=Status.ACTIVATED)

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail={"status": Status.ERROR, "reason": "Bot with this token is already activated"}
        )

    except HTTPException as e:
        logger.error(e, exc_info=True)
        raise e

    except Exception as e:
        logger.error(e, exc_info=True)


@router.post("/drop_bot", status_code=HTTPStatus.CREATED, name="Drop existing bot", responses=delete_bot_resp)
async def drop_bot(bot_data: BaseBotData, db_session: Annotated[AsyncSession, Depends(get_async_session)]) -> BotDeleteResponse:
    if not await db_bot_exists(bot_data.token, db_session):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail={"status": Status.ERROR, "reason": "Bot with this token doesn't exist"})

    await drop_db_bot(bot_data, db_session)
    bot_tg_id: str = bot_data.token.split(':')[0]
    await redis_storage_deletion_manager.find_and_delete_keys(bot_tg_id)
    return BotDeleteResponse(status=Status.DELETED)