from src.bots.db.redis_config import redis, storage


class RedisStorageDeletionKeyManager:
    """Serves for resetting user context for certain bot(AI message history)"""
    def __init__(self, redis_client, redis_storage):
        self.redis_client = redis_client
        self.key_pattern = f"{redis_storage.key_builder.prefix}{redis_storage.key_builder.separator}"

    async def find_and_delete_keys(self, bot_tg_id: str) -> None:
        """Find redis keys and delete"""
        bot_key_pattern: str = f"{self.key_pattern}{bot_tg_id}*"
        keys_to_delete: list = await self.find_keys(bot_key_pattern)
        if keys_to_delete:
            await self.delete_keys(keys_to_delete)

    async def find_keys(self, bot_key_pattern: str) -> list:
        """Search for keys using pattern"""
        cursor = "0"
        found_keys = list()
        while cursor != 0:
            cursor, keys = await self.redis_client.scan(cursor=cursor, match=bot_key_pattern, count=100)
            found_keys.extend(keys)

        return found_keys

    async def delete_keys(self, keys: list):
        """Delete keys from redis DB"""
        for key in keys:
            await self.redis_client.delete(key)


redis_storage_deletion_manager = RedisStorageDeletionKeyManager(redis_client=redis, redis_storage=storage)


