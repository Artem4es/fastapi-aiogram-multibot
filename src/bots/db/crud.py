from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas import BotData
from src.bots.db.database import async_session_maker
from src.bots.db.models import DBBot


async def get_db_bots(db_session: Optional[AsyncSession] = None) -> list[DBBot]:
    """Get activated bots from database"""
    stmt = select(DBBot)
    if not db_session:
        async with async_session_maker() as session:
            res = await session.execute(stmt)
            return list(res.scalars())

    async with async_session_maker() as session:
        res = await session.execute(stmt)
        return list(res.scalars())


async def get_current_bot(bot_tg_id: int, db_session: Optional[AsyncSession] = None) -> Optional[DBBot]:
    """Get alf bot_id by its tg_id"""
    stmt = select(DBBot).where(DBBot.tg_id == bot_tg_id)
    if not db_session:
        async with async_session_maker() as session:
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    res = await db_session.execute(stmt)
    return res.scalar_one_or_none()


async def add_db_bot(bot: BotData, db_session: Optional[AsyncSession] = None) -> None:
    """Add bot to DB"""
    bot_tg_id = int(bot.token.split(":")[0])
    bot = DBBot(assistant_id=bot.assistant_id, token=bot.token, tg_id=bot_tg_id)
    if not db_session:
        async with async_session_maker() as db_session:
            await db_session.merge(bot)
            await db_session.commit()
            return

    await db_session.merge(bot)
    await db_session.commit()


async def db_bot_exists(token: str, db_session: Optional[AsyncSession] = None) -> bool:
    """Check if bot is already in DB"""
    stmt = select(DBBot).where(DBBot.token == token)
    if not db_session:
        async with async_session_maker() as db_session:
            res = await db_session.execute(stmt)
            return bool(res.scalar_one_or_none())

    res = await db_session.execute(stmt)
    return bool(res.scalar_one_or_none())
