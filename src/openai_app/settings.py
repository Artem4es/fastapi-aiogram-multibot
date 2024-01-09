from openai import AsyncOpenAI

from src.config import Settings

settings = Settings()


client = AsyncOpenAI(api_key=settings.openai_key)
