"""Standalone RPC consumer service.

Запускается отдельно от FastAPI:
    python consumer_main.py

FastAPI (main.py) выступает publisher'ом — отправляет RPC-запросы.
Этот сервис — consumer — принимает запросы, обрабатывает и возвращает ответы.
"""

import asyncio
import logging

from shared.log.setup import setup_logging
from src.broker.consumer import rpc_consumer
from shared.broker.queues import ConsumerQueue
from shared.broker.exchanges import ResponseExchange
from src.broker.handlers import ConsumerProcessor

from src.core.config import settings


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    logger = logging.getLogger(__name__)
    logger.info("Starting RPC consumer service")

    from src.core.database import close_db_pool
    from src.core.security import load_keys
    load_keys()

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.AUTH_SIGN_UP.value,
                    callback=ConsumerProcessor.sign_up,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
    finally:
        await close_db_pool()

if __name__ == "__main__":
    asyncio.run(main())
