from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Fastapi and bot app settings"""
    redis_host: str
    redis_port: int

    db_host: str
    db_port: int
    db_name: str
    db_password: str
    db_user: str

    fastapi_host: str
    fastapi_port: int
    fastapi_debug: bool
    fastapi_name: str = "Bot app"

    main_bot_token: str
    base_webhook_url: str
    main_bot_path: str
    main_bot_name: str
    bot_server_host: str
    bot_server_port: int
    other_bots_path: str
    parse_mode: str

    gpt_token_limit: int
    typing_action_duration: int

    openai_key: str
    default_engine: str
    default_temperature: float

    # HNY!
    ids: str
    gop_token: str
    model_config = SettingsConfigDict(env_file=".env")
    # model_config = SettingsConfigDict(env_file=".env.debug")

    @property
    def async_db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?async_fallback=True"
