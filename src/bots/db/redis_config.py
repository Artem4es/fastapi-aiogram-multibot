from aiogram.fsm.storage.redis import DefaultKeyBuilder, Redis, RedisStorage

from src.config import Settings

settings = Settings()

redis = Redis(host=settings.redis_host, port=int(settings.redis_port), decode_responses=True)
storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_bot_id=True))
