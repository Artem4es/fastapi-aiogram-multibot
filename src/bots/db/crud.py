from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas import BotData
from src.bots.db.database import async_session_maker
from src.bots.db.models import BotORM



async def get_db_bots(db_session: Optional[AsyncSession] = None) -> list[BotORM]:
    """Get activated bots from database"""
    stmt = select(BotORM)
    if not db_session:
        async with async_session_maker() as session:
            res = await session.execute(stmt)
            return list(res.scalars())

    async with async_session_maker() as session:
        res = await session.execute(stmt)
        return list(res.scalars())


async def get_current_bot(bot_tg_id: int, db_session: Optional[AsyncSession] = None) -> Optional[BotORM]:
    """Get alf bot_id by its tg_id"""
    stmt = select(BotORM).where(BotORM.tg_id == bot_tg_id)
    try:
        if not db_session:
            async with async_session_maker() as session:
                res = await session.execute(stmt)
                return res.scalar_one_or_none()

        res = await db_session.execute(stmt)
        return res.scalar_one_or_none()

    except Exception as e:
        logger.error(e)


async def add_db_bot(bot_data: BotData, db_session: Optional[AsyncSession] = None) -> None:
    """Add bot to DB"""
    bot_tg_id = int(bot_data.token.split(":")[0])
    bot_orm = BotORM(tg_id=bot_tg_id, **bot_data.model_dump())
    if not db_session:
        async with async_session_maker() as db_session:
            await db_session.merge(bot_orm)
            await db_session.commit()
            return

    await db_session.merge(bot_orm)
    await db_session.commit()


async def db_bot_exists(token: str, db_session: Optional[AsyncSession] = None) -> bool:
    """Check if bot is already in DB"""
    stmt = select(BotORM).where(BotORM.token == token)
    if not db_session:
        async with async_session_maker() as db_session:
            res = await db_session.execute(stmt)
            return bool(res.scalar_one_or_none())

    res = await db_session.execute(stmt)
    return bool(res.scalar_one_or_none())
