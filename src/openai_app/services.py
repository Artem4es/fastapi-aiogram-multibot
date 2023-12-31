import logging

from src.bots.phrases import BotPhrases
from src.bots.utils import token_limit_exceeded
from src.openai_app.settings import client
from src.config import Settings


settings = Settings()
logger = logging.getLogger(__name__)


async def process_question(question: str, context: list[dict]) -> str:
    """Makes request to OpenAI API"""
    try:
        context.append({'role': 'user', 'content': question})
        response = await client.chat.completions.create(
            model=settings.default_engine,
            messages=context
        )

        if token_limit_exceeded(response):
            return BotPhrases.CONTEXT_LIMIT_EXCEEDED

        answer: str = response.choices[0].message.content
        return answer

    except Exception as e:
        logger.error(e)
        return BotPhrases.MAYBE_CONTEXT_EXCEED


