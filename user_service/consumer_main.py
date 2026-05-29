"""Standalone RPC consumer service.

Запускается отдельно от FastAPI:
    python consumer_main.py

FastAPI (main.py) выступает publisher'ом — отправляет RPC-запросы.
Этот сервис — consumer — принимает запросы, обрабатывает и возвращает ответы.
"""

import asyncio
import logging

from shared.log.setup import setup_logging
from user_service.broker.consumer import rpc_consumer
from shared.broker.queues import ConsumerQueue
from shared.broker.exchanges import ResponseExchange
from user_service.broker.consumer_processor import ConsumerProcessor

from user_service.core.config import settings
from user_service.core.database import close_db_pool
from user_service.core.security import load_keys


async def main() -> None:
    setup_logging(level=settings.LOGGING_LEVEL)
    logger = logging.getLogger(__name__)
    logger.info("Starting RPC consumer service")
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

            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.AUTH_SIGN_IN.value,
                    callback=ConsumerProcessor.sign_in,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )

            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.AUTH_REFRESH.value,
                    callback=ConsumerProcessor.refresh,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )

            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.USER_GET_PROFILE.value,
                    callback=ConsumerProcessor.get_profile,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.USER_UPDATE_PROFILE.value,
                    callback=ConsumerProcessor.update_profile,
                    response_exchange_name=ResponseExchange.DEFAULT,
                )
            )
            tg.create_task(
                rpc_consumer.start_consuming(
                    queue_name=ConsumerQueue.USER_DELETE.value,
                    callback=ConsumerProcessor.delete_account,
                    response_exchange_name=ResponseExchange.DEFAULT,
    )
)
    finally:
        await close_db_pool()

if __name__ == "__main__":
    asyncio.run(main())
