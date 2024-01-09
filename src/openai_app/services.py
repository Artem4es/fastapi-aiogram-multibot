import logging

import openai

from src.bots.exceptions.exceptions import OpenAIErrorResolver
from src.bots.phrases import BotPhrases
from src.config import Settings
from src.openai_app.settings import client

settings = Settings()
logger = logging.getLogger(__name__)


async def process_question(question: str, context: list[dict]) -> str:
    """Makes request to OpenAI API"""
    try:
        context.append({"role": "user", "content": question})
        response = await client.chat.completions.create(model=settings.default_engine, messages=context)

        answer: str = response.choices[0].message.content
        return answer

    except openai.BadRequestError as e:
        if OpenAIErrorResolver.token_limit_exceeded(e):
            return BotPhrases.CONTEXT_LIMIT_EXCEEDED

        logger.error(e)
        return BotPhrases.TRY_AGAIN

    except openai.PermissionDeniedError as e:
        logger.error(f"Возможно ругается на российский сервер (надо включить VPN): {e}")
        return BotPhrases.TRY_AGAIN

    except Exception as e:
        logger.error(e)
        return BotPhrases.TRY_AGAIN
