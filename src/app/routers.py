import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.responses import activate_bot_resp
from src.app.schemas import BotActivateResponse, BotData, Status
from src.app.services import create_new_bot
from src.bots.db.crud import db_bot_exists
from src.bots.db.database import get_async_session

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/activate_bot", status_code=HTTPStatus.CREATED, name="Activate new bot in TG", responses=activate_bot_resp)
async def activate_bot(bot_data: BotData, db_session: AsyncSession = Depends(get_async_session)) -> BotActivateResponse:
    """Activate new tg bot using token and Alf assistant id"""
    try:
        if not await db_bot_exists(bot_data.token, db_session):
            await create_new_bot(bot_data, db_session)
            return BotActivateResponse(assistant_id=bot_data.assistant_id, status=Status.ACTIVATED)
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail={"status": Status.ERROR, "reason": "Bot with this token is already activated"}
        )

    except HTTPException as e:
        logger.error(e, exc_info=True)
        raise e

    except Exception as e:
        logger.error(e, exc_info=True)
