from openai import AsyncOpenAI
from src.config import Settings

settings = Settings()


client = AsyncOpenAI(api_key=settings.openai_key)


# async def main():
#   response = await client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#       {"role": "system", "content": "You are a helpful assistant."},
#       {"role": "user", "content": "Who won the world series in 2020?"},
#       {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#       {"role": "user", "content": "Where was it played?"}
#     ]
#   )
#   print(response)
#
# asyncio.run(main())