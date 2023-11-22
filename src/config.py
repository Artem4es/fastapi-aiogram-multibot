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

    alf_gpt_url: str

    main_bot_token: str
    main_bot_assistant_id: int
    base_webhook_url: str
    main_bot_path: str
    bot_server_host: str
    bot_server_port: int
    other_bots_path: str

    app_bearer: str
    gpt_token_limit: int
    typing_action_duration: int
    model_config = SettingsConfigDict(env_file=".env")
