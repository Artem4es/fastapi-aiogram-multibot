import logging
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bots.db.crud import get_current_bot
from src.bots.db.models import BotORM
from src.bots.phrases import BotPhrases
from src.config import Settings

logger = logging.getLogger(__name__)

settings = Settings()


async def update_context(state: FSMContext, answer: str, question: str) -> None:
    """Update context in current chat"""
    user_data: dict = await state.get_data()
    context: list[dict] = user_data["context"]
    user_message = {"role": "user", "content": question}
    gpt_answer = {"role": "assistant", "content": answer}
    context.append(user_message)
    if answer is not None:
        if not any(phrase.value == answer for phrase in BotPhrases):
            context.append(gpt_answer)

    await state.update_data(context=context)


async def reset_context(tg_bot_id: int, state: FSMContext) -> None:
    """Set user_data in FSM context"""
    bot: Optional[BotORM] = await get_current_bot(tg_bot_id)
    user_data = dict(context=[{"role": "system", "content": bot.prompt}])
    await state.set_data(user_data)


def get_key_data(message: Message) -> tuple:
    """Get id for bot, chat and user"""

    bot_id: int = message.bot.id
    chat_id: int = message.chat.id
    user_id: int = message.from_user.id
    return bot_id, chat_id, user_id
