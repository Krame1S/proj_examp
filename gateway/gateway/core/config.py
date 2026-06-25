from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "gateway"
    DEBUG: bool = False
    LOGGING_LEVEL: str = "INFO"

    RABBIT_AMQP: str = "amqp://guest:guest@localhost:5672/"
    REDIS_URL: str = "redis://localhost:6379/0"

    CORS_ORIGINS: str = "*"

    ENABLE_METRICS: bool = True

    # ── OpenTelemetry Tracing ────────────────────────────
    ENABLE_TRACING: bool = False
    OTEL_SERVICE_NAME: str = "my-backend"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://jaeger:4317"
    JWT_ALGORITHM: str = "RS256"
    JWT_PUBLIC_KEY_PATH: str = "/app/keys/public.pem"

    # ── S3 ─────────────────────────────────────────────────────────────────
    # The gateway uploads files directly to S3; the attachment_service only
    # stores the resulting key + metadata.
    S3_ENDPOINT_URL: str = ""          # leave empty for AWS; set for MinIO etc.
    S3_ACCESS_KEY_ID: str = ""
    S3_SECRET_ACCESS_KEY: str = ""
    S3_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = ""
    S3_PUBLIC_URL: str = ""            # e.g. "https://cdn.example.com" or MinIO public base

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()