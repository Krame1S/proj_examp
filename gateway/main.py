import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.api.errors import register_error_handlers
from gateway.api.v1.router import v1_router
from gateway.broker.rpc_publisher import rpc_publisher
from gateway.core.config import settings
from gateway.core.security import load_public_key
from gateway.middleware.logging import LoggingMiddleware
from shared.broker.exchanges import ResponseExchange
from shared.broker.queues import ResponseQueue


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.LOGGING_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────
    setup_logging()
    load_public_key(settings.JWT_PUBLIC_KEY_PATH) 

    await rpc_publisher.connect(
        response_queue_name=ResponseQueue.DEFAULT.value,
        response_exchange_name=ResponseExchange.DEFAULT.value,
    )

    yield

    # ── Shutdown ─────────────────────────────────────
    await rpc_publisher.close()


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(v1_router, prefix="/api")