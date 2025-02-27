from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_URL: str
    model_config = SettingsConfigDict(env_prefix="APP_")
