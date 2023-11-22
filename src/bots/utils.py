from typing import Optional

from src.bots.phrases import BotPhrases
from src.config import Settings

settings = Settings()


def close_token_limit(result) -> str:
    """Checks if context is not exceeding GPT limit"""
    debug_info: dict = result["debugInfo"]
    max_tokens: int = settings.gpt_token_limit
    response: Optional[dict] = debug_info["response"]
    if response is None:
        return BotPhrases.CONTEXT_LIMIT_EXCEEDED

    tokens_used: int = response["usage"]["totalTokens"]
    if max_tokens - tokens_used < 200:
        return BotPhrases.CLOSE_TO_CONTEXT_LIMIT
    return ""
