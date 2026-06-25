from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DEBUG: bool = False
    LOGGING_LEVEL: str = "INFO"

    # ── PostgreSQL ───────────────────────────────────────
    DATABASE_URL: str = ""
    DATABASE_URL_SQLALCHEMY: str = ""
    DB_SCHEMA: str = "attachments"
    DB_MIN_POOL_SIZE: int = 5
    DB_MAX_POOL_SIZE: int = 20

    # ── RabbitMQ ────────────────────────────────────────
    RABBIT_AMQP: str = "amqp://guest:guest@localhost:5672/"

    # ── S3 ───────────────────────────────────────────────
    # Leave all S3_* empty and set MOCK_S3=true (or DEBUG=true) for local dev.
    # Fill in real values when deploying to an environment with an actual bucket.
    S3_ENDPOINT_URL: str = ""
    S3_ACCESS_KEY_ID: str = ""
    S3_SECRET_ACCESS_KEY: str = ""
    S3_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = ""
    S3_PUBLIC_URL: str = ""


settings = Settings()
