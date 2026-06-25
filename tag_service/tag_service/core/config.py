from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    LOGGING_LEVEL: str = "INFO"

    # ── PostgreSQL ───────────────────────────────────────
    DATABASE_URL: str = ""
    DATABASE_URL_SQLALCHEMY: str = ""
    DB_SCHEMA: str = "tags"
    DB_MIN_POOL_SIZE: int = 5
    DB_MAX_POOL_SIZE: int = 20

    # ── RabbitMQ ────────────────────────────────────────
    RABBIT_AMQP: str = "amqp://guest:guest@localhost:5672/"

    # ── Redis ────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()
