from src.openai_app.settings import client
from src.config import Settings


settings = Settings()


async def process_question(question: str, context: list[dict]) -> str:
    """Makes request to OpenAI API"""
    context.append({'role': 'user', 'content': question})
    response = await client.chat.completions.create(
        model=settings.default_engine,
        messages=context
    )
    answer: str = response.choices[0].message.content
    return answer
