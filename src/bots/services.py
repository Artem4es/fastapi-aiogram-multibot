import logging
from http import HTTPStatus
from typing import Optional

import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bots.db.crud import get_current_bot
from src.bots.db.models import DBBot
from src.bots.exceptions.exceptions import ProcessQuestionError
from src.bots.utils import close_token_limit
from src.config import Settings

logger = logging.getLogger(__name__)

settings = Settings()


async def process_question(
    question: str, bot_id: int, context: Optional[str], alf_assistant_id: int, chat_uid: Optional[str]
) -> Optional[dict[str, str]]:
    """Makes request to ALF GPT API"""
    token: str = settings.app_bearer
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "source": question,
        "assistant_id": alf_assistant_id,
    }
    if chat_uid:
        request_data["chat_uid"] = chat_uid

    if context:
        request_data["context"] = context

    try:
        logger.info(f"Bot_id: {bot_id}. Отправляю запрос на {settings.alf_gpt_url}. Запрос: {request_data} | Заголовки {headers}")
        async with aiohttp.ClientSession(headers=headers) as client:
            async with client.post(url=settings.alf_gpt_url, data=request_data) as resp:
                if resp.status == HTTPStatus.OK:
                    result = await resp.json()
                    chat_uid: str = result.get("chatUid")
                    answer: str = result.get("payload")
                    word_limit: str = close_token_limit(result)
                    if word_limit:
                        if not answer:
                            answer = word_limit
                        else:
                            answer = word_limit + answer

                    logger.info(f"Bot_id: {bot_id}. Ответ успешно получен: {chat_uid}: {answer}")
                    return {"chat_uid": chat_uid, "answer": answer}

                raise ProcessQuestionError(f"Bot_id: {bot_id}. Ответ эндпоинта GPT ALF != {HTTPStatus.OK}. Ответ: {resp.status}")

    except Exception as e:
        raise ProcessQuestionError(f"Bot_id: {bot_id}. Не удалось получить ответ от эндпоинта GPT ALF: {e}")


async def update_context(state: FSMContext, resp: dict, question: str) -> None:
    """Update context in current chat"""
    answer: str = resp["answer"]
    user_data: dict = await state.get_data()
    current_chat_data = user_data.get("current_chat")
    chat_uid: str = resp["chat_uid"]
    if not current_chat_data:
        fresh_context: str = f"{question}\n{answer}"
        current_chat = dict(uid=chat_uid, context=fresh_context)
        await state.update_data(current_chat=current_chat)
        return

    current_chat_context: str = current_chat_data["context"]
    fresh_context: str = f"{current_chat_context}\n{question}\n{answer}"
    current_chat = dict(uid=chat_uid, context=fresh_context)
    await state.update_data(current_chat=current_chat)


async def set_user_data(tg_bot_id: int, state: FSMContext) -> None:
    """Set user_data in FSM context"""
    bot: DBBot = await get_current_bot(tg_bot_id)
    alf_assistant_id: int = bot.assistant_id
    user_data = dict(assistant_id=alf_assistant_id, current_chat=dict(uid=None, context=None))
    await state.set_data(user_data)


def get_key_data(message: Message) -> tuple:
    """Get id for bot, chat and user"""

    bot_id: int = message.bot.id
    chat_id: int = message.chat.id
    user_id: int = message.from_user.id
    return bot_id, chat_id, user_id
