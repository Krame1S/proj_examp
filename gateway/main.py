import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from shared.broker.exchanges import ResponseExchange
from shared.broker.queues import ResponseQueue
from shared.log.setup import setup_logging
from shared.metrics.setup import setup_tracing
from shared.metrics.tracing import TracingMiddleware

from gateway.api.errors import register_error_handlers
from gateway.api.v1.router import v1_router
from gateway.api.v1.ws import redis_listener
from gateway.broker.rpc_publisher import rpc_publisher
from gateway.core.config import settings
from gateway.core.security import load_public_key
from gateway.middleware.logging import LoggingMiddleware
from gateway.middleware.metrics import MetricsMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────
    setup_logging(level=settings.LOGGING_LEVEL)
    if settings.ENABLE_TRACING:
        setup_tracing(service_name="gateway")
    load_public_key(settings.JWT_PUBLIC_KEY_PATH)

    await rpc_publisher.connect(
        response_queue_name=ResponseQueue.DEFAULT.value,
        response_exchange_name=ResponseExchange.DEFAULT.value,
    )

    listener_task = asyncio.create_task(redis_listener())

    yield

    listener_task.cancel()
    with suppress(asyncio.CancelledError):
        await listener_task

    await rpc_publisher.close()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.ENABLE_METRICS:
    app.add_middleware(MetricsMiddleware)

if settings.ENABLE_TRACING:
    app.add_middleware(TracingMiddleware)

app.add_middleware(LoggingMiddleware)

app.include_router(v1_router, prefix="/api")

if settings.ENABLE_METRICS:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
