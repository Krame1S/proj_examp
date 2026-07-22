from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    LOGGING_LEVEL: str = "INFO"
    DATABASE_URL: str = ""
    DB_SCHEMA: str = "categories"
    DB_MIN_POOL_SIZE: int = 5
    DB_MAX_POOL_SIZE: int = 20
    RABBIT_AMQP: str = "amqp://guest:guest@localhost:5672/"


settings = Settings()
