import asyncio
import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bots.core.questions import (
    QuestionKeyBuilder,
    SetStorage, PendingQuestionManager,
)
from src.bots.phrases import BotPhrases
from src.bots.services import get_key_data, reset_context, update_context
from src.config import Settings
from src.openai_app.services import process_question

question_key_builder = QuestionKeyBuilder()
question_key_storage = SetStorage()
question_manager = PendingQuestionManager(key_builder=question_key_builder, storage=question_key_storage)

main_bot_router = Router()
multi_bot_router = Router()

new_handler = Router()
logger = logging.getLogger(__name__)

settings = Settings()


@multi_bot_router.message(CommandStart())
@main_bot_router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    """User sent '/start' command"""
    user_data: dict = await state.get_data()
    bot_id, chat_id, user_id = get_key_data(message)
    key: str = question_manager.build_key(bot_id, chat_id, user_id)
    if not user_data:
        await reset_context(bot_id, state)

    if not question_manager.question_pending(key):
        await message.answer(text=BotPhrases.hello(message.from_user.first_name))

    else:
        await message.answer(text=BotPhrases.WAIT_PREVIOUS_QUESTION)
        await message.chat.do(action="typing")


@multi_bot_router.message(Command("refresh_history"))
@main_bot_router.message(Command("refresh_history"))
async def refresh_history(message: Message, state: FSMContext) -> None:
    """Clear context history in chat"""
    try:
        user_data: dict = await state.get_data()
        bot_id, chat_id, user_id = get_key_data(message)
        key: str = question_manager.build_key(bot_id, chat_id, user_id)
        if not user_data:
            await message.answer(text=BotPhrases.START_FIRST)

        else:
            if not question_manager.question_pending(key):
                await reset_context(bot_id, state)
                await message.answer(text=BotPhrases.CONTEXT_CLEANED)

            else:
                await message.answer(text=BotPhrases.WAIT_PREVIOUS_QUESTION)
                await message.chat.do(action="typing")

    except Exception as e:
        logger.error(e, exc_info=True)
        await message.answer(text=BotPhrases.TRY_AGAIN)


@multi_bot_router.message()
@main_bot_router.message()
async def user_question(message: Message, state: FSMContext) -> None:
    """User asked something"""
    try:
        user_data: dict = await state.get_data()
        context: list[dict] = user_data.get("context")
        bot_id, chat_id, user_id = get_key_data(message)
        if not context:
            await reset_context(bot_id, state)
            user_data: dict = await state.get_data()
            context = user_data["context"]

        question: str = message.text
        if question is None:  # needed for adding/drop and other unexpected actions group member handling
            return

        question_key: str = question_manager.build_key(bot_id, chat_id, user_id)
        if not question_manager.question_pending(question_key):
            with question_manager.add_question(question_key):
                task = asyncio.create_task(process_question(question=question, context=context))
                while not task.done():
                    await message.chat.do(action="typing")
                    await asyncio.sleep(settings.typing_action_duration)

                answer: str = task.result()
                await update_context(state, answer, question)

                await message.answer(text=answer, parse_mode=settings.parse_mode)

        else:
            await message.answer(text=BotPhrases.WAIT_PREVIOUS_QUESTION)
            await message.chat.do(action="typing")

    except Exception as e:
        logger.error(e, exc_info=True)
        await message.answer(text=BotPhrases.TRY_AGAIN)


@multi_bot_router.callback_query()
@main_bot_router.callback_query()
async def handle_unhandled_callback(callback: CallbackQuery):
    """
    If none of the call_back handlers has triggered - this one triggers, disabling the button pending.
    This handler has to be the LAST among all handlers!
    """
    await callback.answer()
