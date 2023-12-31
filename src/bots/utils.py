from src.config import Settings

settings = Settings()


def token_limit_exceeded(response) -> bool:
    """Token limit has been reached need to refresh dialog context"""
    usage = response.usage
    tokens_used: int = usage.total_tokens
    return tokens_used > settings.gpt_token_limit
